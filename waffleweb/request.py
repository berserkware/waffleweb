import os
import importlib
import waffleweb
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from urllib.parse import urlparse
from waffleweb.cookie import Cookies
from waffleweb.response import HTTP404, FileResponse, HTTPResponse, HTTPResponsePermenentRedirect, HTTPResponseRedirect, JSONResponse, render
from waffleweb.static import StaticHandler
from waffleweb.template import renderErrorPage, renderTemplate

class Request():
    def __init__(self, requestHeaders, clientIP, wsgi=False):
        self.wsgi = wsgi
        self.headers = {}
        self.clientIP = clientIP
        self.requestHeaders = requestHeaders

        self.postData = {}

        #Splits the request into it's seporate headers and adds it to a dictionary.
        splitHeaders = requestHeaders.split('\n')
        for line in splitHeaders:
                splitLine = line.strip().split(' ')
                self.headers[str(splitLine[0][:(len(splitLine[0]) - 1)])] = ' '.join(splitLine[1:])

        #adds forms data to the postData variable
        if self.method == 'POST':
            self._getPostData()

        if 'Cookie' in self.headers.keys():
            self.cookies = Cookies(self.headers['Cookie'])
        else:
            self.cookies = Cookies()

    def _getPostData(self):
        if self.content != '':
            #If Content-Type is not in headers then make it 'application/x-www-form-urlencoded'
            if 'Content-Type' not in self.headers.keys():
                self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
                
            #Spits the form values and adds them to a dictionary if Content-Type is 'application/x-www-form-urlencoded'
            if self.headers['Content-Type'] == 'application/x-www-form-urlencoded':
                formValues = self.content.split('&')
                #For every form value add it to a dictionary called postData
                for value in formValues:
                    try:
                        key, value = value.split('=')
                        self.postData[str(key.strip('\n'))] = str(value.strip('\n'))
                    except ValueError:
                        pass

            #If the contentType is equal to 'multipart/form-data' split it and add it to a dictionary
            elif self.headers['Content-Type'].split(';')[0] == 'multipart/form-data':
                #gets the boundry
                contentTypeHeader = self.headers['Content-Type'].split(';')
                boundary = 'boundary'

                for index, keyvalue in enumerate(contentTypeHeader):
                    if index != 0:
                        key, value = keyvalue.split('=')
                        if key.strip() == 'boundary':
                            boundary = value

                #splits the form values by the boundry
                splitFormValues = self.content.split('--' + boundary)

                #goes through all the split values
                for formValue in splitFormValues:
                    if formValue != '\n' and formValue != '--\n':
                        #splits the data into its seporate headers and removes empty items
                        dataWithSpaces = formValue.split('\n')
                        data = []
                        for i in dataWithSpaces:
                            if i != '':
                                data.append(i)

                        #Goes through all the headers of the formValues
                        for field in data[0].split(';'):
                            #checks to see if its a header
                            if field.split(':')[0] == '\nContent-Disposition:':
                                continue
                            #if not then get the name of field
                            else:
                                try:
                                    key, value = field.split('=')
                                    if key.strip() == 'name':
                                        name = value.strip('"')
                                except ValueError:
                                    pass

                        #adds to postData
                        self.postData[str(name)] = data[-1]

    @property
    def path(self):
        return self.requestHeaders.split('\n')[0].split()[1]

    @property
    def method(self):
        return self.requestHeaders.split('\n')[0].split()[0]

    @property
    def HTTPVersion(self):
        return self.requestHeaders.split('\n')[0].split()[2]

    @property
    def content(self):
        splitContent = []
        isContent = False

        #this splits the requests by the \r
        for line in self.requestHeaders.split('\r'):
            #check if isContent is True to start adding to the content
            if isContent == True:
                splitContent.append(line)

            #checks if the line is equest = '\n'. this splits the request into content and header
            if line == '\n':
                isContent = True

        #returns the joins content
        return ''.join(splitContent)

class RequestHandler:
    '''Handles a requests, Returns response'''
    def __init__(self, request: Request, debug=False):
        self.request = request
        self.apps = waffleweb.defaults.APPS
        self.debug = debug

    def _405MethodNotAllowed(self, allowedMethods) -> HTTPResponse:
        '''Returns a 405 response'''
        methods = ', '.join(allowedMethods)
        if self.debug:
            render = renderErrorPage(
                mainMessage='404 Method Not Allowed',
                subMessage=f'Allowed Methods: {methods}',
            )
            return HTTPResponse(None, render, status=405, headers=f'Allow: {methods}') 
        else:
            return HTTPResponse(None, status=405, headers=f'Allow: {methods}') 

    def _getArg(self, index, part) -> tuple:
        '''
        Gets the kwargs and converts them to their type.
        returns a tuple with the name and type
        '''
        kwargName = ''
        kwargValue = None

        if part[1] == 'int':
            kwargName = str(part[0])
            kwargValue = int(self.splitRoot[index])
        elif part[1] == 'float':
            kwargName = str(part[0])
            kwargValue = float(self.splitRoot[index])
        else:
            kwargName = str(part[0])
            kwargValue = str(self.splitRoot[index])

        return (kwargName, kwargValue)

    def _splitURL(self) -> tuple:
        reqPath = urlparse(self.request.path).path

        #gets the root and file extenstion
        root, ext = os.path.splitext(reqPath)
        splitRoot = root.strip('/').split('/')

        return (root, splitRoot, ext)

    def _getView(self):
        '''Finds a view matching the request url, Returns view and the views kwargs.'''

        self.root, self.splitRoot, self.ext = self._splitURL()
        self.root = self.root.strip('/')

        #Searches through all the apps to match the url
        for app in self.apps:
            app = app['app']
            for view in app.views:
                urlMatches = True
                viewKwargs = {}
                if view['path'] == self.root:
                    return (view, {})

                #checks if length of the view's split path is equal to the length of the split request request path
                if len(view['splitPath']) == len(self.splitRoot) and view['splitPath'] != ['']:
                    for index, part in enumerate(view['splitPath']):
                        #checks if path part is equal to the split request path part at the same index
                        if part != self.splitRoot[index] and type(part) == str:
                            urlMatches = False
                            break
                        
                        #makes sure not static file
                        if self.ext == '':
                            #adds args to view kwargs if part is list
                            if type(part) == list:
                                kwarg = self._getArg(index, part)
                                viewKwargs[kwarg[0]] = kwarg[1]

                    if urlMatches:
                        return (view, viewKwargs)
        
        raise HTTP404


    def _handleGet(self, view, kwargs):
        if 'GET' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)

    def _handleHead(self, view, kwargs):
        #Checks if GET or HEAD is in allowed methods
        if 'GET' not in view['allowedMethods'] and 'HEAD' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        newView = view['view'](self.request, **kwargs)

        if type(newView) == HTTPResponse:
            newView.content = None
        elif newView == JSONResponse:
            newView.json = None
        elif newView == FileResponse:
            newView.fileObj = None

        return newView

    def _handlePost(self, view, kwargs):
        if 'POST' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)

    def _handlePut(self, view, kwargs):
        if 'PUT' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)

    def _handleDelete(self, view, kwargs):
        if 'DELETE' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)

    def _handleConnect(self, view, kwargs):
        if 'CONNECT' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)

    def _handleOptions(self, view, kwargs):
        #Checks if GET or OPTIONS is in allowed methods
        if 'GET' not in view['allowedMethods'] and 'OPTIONS' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        if view is None:
            methods = ', '.join(['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'])
            return HTTPResponse(status=204, headers=f'Allow: {methods}') 

        methods = ', '.join(view['allowedMethods'])
        return HTTPResponse(status=204, headers=f'Allow: {methods}') 

    def _handleTrace(self, view, kwargs):
        if 'TRACE' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)

    def _handlePatch(self, view, kwargs):
        if 'PATCH' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)


    def getResponse(self):
        '''Gets a response to a request, retuerns Response.'''

        root, splitRoot, ext = self._splitURL()
        if ext == '':
            #if the route is equal to '*' return a OPTIONS response
            if root == '*':
                return self._handleOptions(None, {})

            try:
                #If the view path ends without a slash and the client goes to that page with a slash raise 404
                view, kwargs = self._getView()
                if view['unstripedPath'].endswith('/') == False and root.endswith('/'):
                    raise HTTP404
                #if the view path ends with a slash and the client goes to that page without a slash redirect to page without slash
                elif view['unstripedPath'].endswith('/') and root.endswith('/') == False:
                    return HTTPResponsePermenentRedirect(f'{root}/')

                #Gets methods and runs it's handle function
                if self.request.method == 'GET':
                    return self._handleGet(view, kwargs)
                elif self.request.method == 'HEAD':
                    return self._handleHead(view, kwargs)
                elif self.request.method == 'POST':
                    return self._handlePost(view, kwargs)
                elif self.request.method == 'PUT':
                    return self._handlePut(view, kwargs)
                elif self.request.method == 'DELETE':
                    return self._handleDelete(view, kwargs)
                elif self.request.method == 'CONNECT':
                    return self._handleConnect(view, kwargs)
                elif self.request.method == 'POST':
                    return self._handlePost(view, kwargs)
                elif self.request.method == 'OPTIONS':
                    return self._handleOptions(view, kwargs)
                elif self.request.method == 'TRACE':
                    return self._handleTrace(view, kwargs)
                elif self.request.method == 'PATCH':
                    return self._handlePatch(view, kwargs)
                else:
                    if self.debug:
                        render = renderErrorPage(
                            mainMessage='501 Not Implemented Error', 
                            subMessage=f'The requested method is not implemented',
                            traceback=f'Method:{self.request.method}',
                            )
                        return HTTPResponse(None, render, status=501) 
                    else:
                        return HTTPResponse(None, 'Not Implemented Error', status=501) 
            except HTTP404:
                if self.debug:
                    #Gets all searched views.
                    searchedViews = []
                    for app in self.apps:
                        app = app['app']
                        for view in app.views:
                            path = view['unstripedPath']

                            #turns the arrows into one html cannot render
                            path = path.replace('<', '&lt;')
                            path = path.replace('>', '&gt;')
                            searchedViews.append(path)

                    page = renderErrorPage(
                        mainMessage='404 Page Not Found', 
                        subMessage=f'The requested page could not be found',
                        traceback=f'Views searched:<br>{"<br>".join(searchedViews)}',
                        )
                    return HTTPResponse(None, page, status=404)
                else:
                    if hasattr(settings, 'file404'):
                        file404 = getattr(settings, 'file404')

                    page = renderTemplate(file404)
                    return HTTPResponse(None, page, status=404)
        else:
            try:
                handler = StaticHandler(self.request, root, splitRoot, ext)
                return handler.findFile()
            except HTTP404:
                #if debug mode is on show errors
                if self.debug:
                    page = renderErrorPage(mainMessage='404 File Not Found<br>', subMessage='The requested file could not be found')
                    return HTTPResponse(None, page, status=404)
                else:
                    if hasattr(settings, 'file404'):
                        file404 = getattr(settings, 'file404')

                    page = renderTemplate(file404)
                    return HTTPResponse(None, page, status=404)