import os

from urllib.parse import urlparse

from waffleweb.response import HTTP404, FileResponse, HTTPResponse, JSONResponse
from waffleweb.static import StaticHandler

class Request():
    def __init__(self, requestHeaders, clientIP):
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
    def host(self):
        return self.headers['Host']

    @property
    def userAgent(self):
        return self.headers['User-Agent']

    @property
    def accept(self):
        return self.headers['Accept']

    @property
    def acceptLanguage(self):
        return self.headers['Accept-Language']

    @property
    def acceptEncoding(self):
        return self.headers['Accept-Encoding']

    @property
    def connection(self):
        return self.headers['Connection']

    @property
    def cookie(self):
        return self.headers['Cookie']

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
    def __init__(self, request: Request, apps: list):
        self.request = request
        self.apps = apps

    def _405MethodNotAllowed(self, allowedMethods) -> HTTPResponse:
        '''Returns a 405 response'''
        methods = ', '.join(allowedMethods)
        return HTTPResponse(status=405, headers=f'Allow: {methods}') 

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
        root = root.strip('/')
        splitRoot = root.split('/')

        return (root, splitRoot, ext)

    def _getView(self):
        '''Finds a view matching the request url, Returns view and the views kwargs.'''

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
                        
                        #adds args to view kwargs if part is list
                        if type(part) == list:
                            kwarg = self._getArg(index, part)
                            viewKwargs[kwarg[0]] = kwarg[1]

                    if urlMatches:
                        return (view, viewKwargs)
        
        raise HTTP404

    def _handleHead(self, view, kwargs):
        if 'HEAD' not in view['allowedMethods']:
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

    def _handleGet(self, view, kwargs):
        if 'GET' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)

    def _handlePost(self, view, kwargs):
        if 'POST' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view['allowedMethods'])

        return view['view'](self.request, **kwargs)

    def _handleOptions(self, view, kwargs):
        if view is None:
            methods = ', '.join(['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'])
            return HTTPResponse(status=204, headers=f'Allow: {methods}') 

        methods = ', '.join(view['allowedMethods'])
        return HTTPResponse(status=204, headers=f'Allow: {methods}') 

    def getResponse(self):
        '''Gets a response to a request, retuerns Response.'''

        self.root, self.splitRoot, self.ext = self._splitURL()
        if self.ext == '':
            #if the route is equal to '*' return a OPTIONS response
            if self.root == '*':
                return self._handleOptions(None, {})

            try:
                view, kwargs = self._getView()

                #Gets methods and runs it handle function
                if self.request.method == 'GET':
                    return self._handleGet(view, kwargs)
                elif self.request.method == 'HEAD':
                    return self._handleHead(view, kwargs)
                elif self.request.method == 'POST':
                    return self._handlePost(view, kwargs)
                elif self.request.method == 'OPTIONS':
                    return self._handleOptions(view, kwargs)
                else:
                    return HTTPResponse('Not Implemented Error', status=501) 
            except HTTP404:
                return HTTPResponse('The requested page could not be found', status=404)
        else:
            try:
                handler = StaticHandler(self.root, self.splitRoot, self.ext)
                return handler.findFile()
            except HTTP404:
                return HTTPResponse('The requested file could not be found', status=404)