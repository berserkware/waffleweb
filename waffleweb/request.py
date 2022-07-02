import os
import importlib
import waffleweb
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from urllib.parse import urlparse, unquote
from waffleweb.cookie import Cookies
from waffleweb.response import HTTP404, FileResponse, HTTPResponse, HTTPResponsePermenentRedirect, JSONResponse
from waffleweb.static import getStaticFileResponse
from waffleweb.template import renderErrorPage, renderTemplate
from waffleweb.files import File
from waffleweb.parser import parseBody, parseHeaders, parsePost

class Request:
    def __init__(self, rawRequest, IP, wsgi=False):
        self.rawRequest = rawRequest
        self.wsgi = wsgi
        self.FILES = {}
        self.META = {}
        self.IP = IP
        self.POST = {}
        self.URL_PARAMS = {}

        if self.wsgi == False:
            self.META = self.META | parseHeaders(self.rawRequest)
        else:
            self.META = self.rawRequest

        self._getURLParams()
        self.body = self._getBody()

        #adds forms data to the postData variable
        if self.method == 'POST' or self.method == 'PUT':
            self._getPostData()

        if 'COOKIE' in self.META.keys():
            self.COOKIES = Cookies(self.META['COOKIE'])
        elif 'HTTP_COOKIE' in self.META.keys():
            self.COOKIES = Cookies(self.META['HTTP_COOKIE'])
        else:
            self.COOKIES = Cookies()

    def _getPostData(self):
        try:
            contentType = self.META['CONTENT_TYPE']
        except KeyError:
            contentType = 'application/x-www-form-urlencoded'

        post, files = parsePost(self.body, contentType)
        self.POST = self.POST | post
        self.FILES = self.FILES | files

    def _getURLParams(self):
        splitPath = self.path.split('?')

        argString = '?'.join(splitPath[1:])

        splitArgs = argString.split('&')

        for arg in splitArgs:
            try:
                name, value = arg.split('=')
                self.URL_PARAMS[str(name)] = str(value)
            except ValueError:
                pass


    def _getBody(self):
        if self.wsgi == False:
            return parseBody(self.rawRequest)
        else:
            length = int(self.META.get('CONTENT_LENGTH', '0'))
            body = self.META['wsgi.input'].read(length)
            return body

    @property
    def path(self):
        if self.wsgi == False:
            return unquote(self.rawRequest.split(b'\n')[0].split()[1].decode())
        else:
            return unquote(self.META['RAW_URI'])

    @property
    def method(self):
        if self.wsgi == False:
            return self.rawRequest.split(b'\n')[0].split()[0].decode()
        else:
            return self.META['REQUEST_METHOD']

    @property
    def HTTPVersion(self):
        if self.wsgi == False:
            return self.rawRequest.split(b'\n')[0].split()[2].decode()
        return 'N/A'

class RequestHandler:
    '''Handles a requests.'''
    def __init__(self, request: Request, debug=False):
        self.request = request
        self.apps = waffleweb.defaults.APPS
        self.debug = debug

    def _getArg(self, index, part) -> tuple:
        '''
        Gets the kwargs and converts them to their type.
        returns a tuple with the name and type
        '''
        kwargName = ''
        kwargValue = None

        if part[1] == 'int':
            kwargName = str(part[0])
            try:
                kwargValue = int(self.splitRoot[index])
            except ValueError:
                kwargValue = str(self.splitRoot[index])
        elif part[1] == 'float':
            kwargName = str(part[0])
            try:
                kwargValue = float(self.splitRoot[index])
            except ValueError:
                kwargValue = str(self.splitRoot[index])
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

    def getView(self):
        '''Finds a view matching the request url, Returns view and the views kwargs.'''

        self.root, self.splitRoot, self.ext = self._splitURL()
        self.root = self.root.strip('/')

        #Searches through all the apps to match the url
        for app in self.apps:
            app = app['app']
            for view in app.views:
                urlMatches = True
                viewKwargs = {}
                if view.path == self.root:
                    return (view, {})

                #checks if length of the view's split path is equal to the length of the split request request path
                if len(view.splitPath) == len(self.splitRoot) and view.splitPath != ['']:
                    for index, part in enumerate(view.splitPath):
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
        if 'GET' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        return view.view(self.request, **kwargs)

    def _handleHead(self, view, kwargs):
        #Checks if GET or HEAD is in allowed methods
        if 'GET' not in view.allowedMethods and 'HEAD' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        newView = view.view(self.request, **kwargs)

        if type(newView) == HTTPResponse:
            newView.content = ''
        elif newView == JSONResponse:
            newView.json = {}
        elif newView == FileResponse:
            newView.fileObj = None

        return newView

    def _handlePost(self, view, kwargs):
        if 'POST' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        return view.view(self.request, **kwargs)

    def _handlePut(self, view, kwargs):
        if 'PUT' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        return view.view(self.request, **kwargs)

    def _handleDelete(self, view, kwargs):
        if 'DELETE' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        return view.view(self.request, **kwargs)

    def _handleConnect(self, view, kwargs):
        if 'CONNECT' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        return view.view(self.request, **kwargs)

    def _handleOptions(self, view, kwargs):
        #Checks if GET or OPTIONS is in allowed methods
        if 'GET' not in view.allowedMethods and 'OPTIONS' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        if view is None:
            methods = ', '.join(['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'])
            res = HTTPResponse(status=204) 
            res.headers['Allow'] = methods
            return res

        methods = ', '.join(view.allowedMethods)
        res = HTTPResponse(status=204) 
        res.headers['Allow'] = methods
        return res

    def _handleTrace(self, view, kwargs):
        if 'TRACE' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        return view.view(self.request, **kwargs)

    def _handlePatch(self, view, kwargs):
        if 'PATCH' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view.allowedMethods)

        return view.view(self.request, **kwargs)

    def getErrorHandler(self, response=None, statusCode=None):
        #Goes through all the apps errorHandlers
        for app in self.apps:
            app = app['app']
            for handler in app.errorHandlers:
                try:
                    #Checks to see if the handlers code is the same as the status Code
                    if handler.statusCode == statusCode:
                        return handler.view(self.request)
                    #Checks to see the the response's status code is equal to the handlers code
                    elif response.statusCode == handler.statusCode:
                        return handler.view(self.request)
                except AttributeError:
                    pass
        return response

    def _handle404View(self):
        if self.debug:
            #Gets all searched views.
            searchedViews = []
            for app in self.apps:
                app = app['app']
                for view in app.views:
                    path = view.unstripedPath

                    #turns the arrows into one html cannot render
                    path = path.replace('<', '&lt;')
                    path = path.replace('>', '&gt;')
                    searchedViews.append(path)

            page = renderErrorPage(
                mainMessage='404 Page Not Found', 
                subMessage=f'The requested page could not be found',
                traceback=f'Views searched:<br>{"<br>".join(searchedViews)}',
                )
            return HTTPResponse(content=page, status=404)
        else:
            response = self.getErrorHandler(statusCode=404)

            if response is None:
                return HTTPResponse(content='404 The requested page could not be found.', status=404)
            else:
                return response

    def _405MethodNotAllowed(self, allowedMethods) -> HTTPResponse:
        '''Returns a 405 response'''
        methods = ', '.join(allowedMethods)
        if self.debug:
            render = renderErrorPage(
                mainMessage='405 Method Not Allowed',
                subMessage=f'Allowed Methods: {methods}',
            )
            res = HTTPResponse(content=render, status=405) 
            res.headers['Allow'] = methods
            return res
        else:
            response = self.getErrorHandler(statusCode=405)
            if response == None:
                res = HTTPResponse(content='405 Method not Allowed', status=405) 
                res.headers['Allow'] = methods
                return res
            else:
                return response

    def _501NotImplementedError(self):
        if self.debug:
            render = renderErrorPage(
                mainMessage='501 Not Implemented Error', 
                subMessage=f'The requested method is not implemented',
                traceback=f'Method:{self.request.method}',
            )
            return HTTPResponse(content=render, status=501) 
        else:
            response = self.getErrorHandler(statusCode=501)
            if response == None:
                return HTTPResponse(content='Not Implemented Error', status=501)
            else:
                return response

    def getResponse(self):
        '''Gets a response to a request, retuerns Response.'''

        root, splitRoot, ext = self._splitURL()
        if ext == '':
            #if the route is equal to '*' return a OPTIONS response
            if root == '*':
                return self._handleOptions(None, {})

            try:
                #If the view path ends without a slash and the client goes to that page with a slash raise 404
                view, kwargs = self.getView()
                if view.unstripedPath.endswith('/') == False and root.endswith('/'):
                    raise HTTP404
                #if the view path ends with a slash and the client goes to that page without a slash redirect to page without slash
                elif view.unstripedPath.endswith('/') and root.endswith('/') == False:
                    #Gets the url params and adds them to the redirected url
                    paramsSplit = self.request.path.split('?')
                    params = (f'?{"?".join(paramsSplit[1:])}' if len(paramsSplit) >= 2 else '')
                    return HTTPResponsePermenentRedirect(f'{root}/{params}')

                #Gets methods and runs it's handle function
                if self.request.method == 'GET':
                    response = self._handleGet(view, kwargs)
                elif self.request.method == 'HEAD':
                    response = self._handleHead(view, kwargs)
                elif self.request.method == 'POST':
                    response = self._handlePost(view, kwargs)
                elif self.request.method == 'PUT':
                    response = self._handlePut(view, kwargs)
                elif self.request.method == 'DELETE':
                    response = self._handleDelete(view, kwargs)
                elif self.request.method == 'CONNECT':
                    response = self._handleConnect(view, kwargs)
                elif self.request.method == 'POST':
                    response = self._handlePost(view, kwargs)
                elif self.request.method == 'OPTIONS':
                    response = self._handleOptions(view, kwargs)
                elif self.request.method == 'TRACE':
                    response = self._handleTrace(view, kwargs)
                elif self.request.method == 'PATCH':
                    response = self._handlePatch(view, kwargs)
                else:
                    response = self._501NotImplementedError()
                    
                response = self.getErrorHandler(response)
                return response
                
            except HTTP404:
                return self._handle404View()
        else:
            try:
                return getStaticFileResponse(self.request, root, ext)
            except HTTP404:
                return self._handle404View()
                