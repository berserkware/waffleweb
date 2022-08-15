import os
import importlib
import waffleweb
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from urllib.parse import urlparse, unquote
from waffleweb.errorResponses import notImplementedError, pageNotFound
from waffleweb.cookie import Cookies
from waffleweb.response import HTTP404, FileResponse, HTTPResponse, HTTPResponsePermenentRedirect, JSONResponse
from waffleweb.static import getStaticFileResponse
from waffleweb.template import renderErrorPage
from waffleweb.parser import parseBody, parseHeaders, parsePost
from waffleweb.datatypes import MultiValueOneKeyDict

class Request:
    def __init__(self, rawRequest, IP, wsgi=False):
        self.rawRequest = rawRequest
        self.wsgi = wsgi
        self.FILES = {}
        self.META = MultiValueOneKeyDict()
        self.IP = IP
        self.POST = {}
        self.URL_PARAMS = {}

        if self.wsgi == False:
            self.META._data.update(parseHeaders(self.rawRequest)._data)
        else:
            self.META = MultiValueOneKeyDict(self.rawRequest)

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
            length = int(self.META.get('CONTENT_LENGTH', default='0'))
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
    def __init__(self, request: Request, debug=False, app=None):
        self.request = request
        self.app = app
        
        if app is None:
            self.app = waffleweb.currentRunningApp
            self.views = waffleweb.currentRunningApp.views
            self.errorHandlers = waffleweb.currentRunningApp.errorHandlers
        else:
            self.views = app.views
            self.errorHandlers = app.errorHandlers
            
        self.debug = debug

    def _getArg(self, index, part) -> tuple:
        '''
        Gets the kwargs and converts them to their type.
        returns a tuple with the name and value
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

    def findView(self):
        '''Finds a view matching the request url, Returns view and the views kwargs.'''

        self.root, self.splitRoot, self.ext = self._splitURL()
        self.root = self.root.strip('/')

        #Searches through all the views to match the url
        for view in self.views:
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
        
        allowedMethods = view.allowedMethods.copy()
        if 'GET' in allowedMethods:
            if 'HEAD' not in allowedMethods:
                allowedMethods.append('HEAD')
            if 'OPTIONS' not in allowedMethods:
                allowedMethods.append('OPTIONS')
        
        methods = ', '.join(allowedMethods)
        res = HTTPResponse(status=204) 
        res.headers['Allow'] = methods
        return res

    def _handleMethod(self, method, view, kwargs):
        if method == 'HEAD':
            return self._handleHead(view, kwargs)
        elif method == 'OPTIONS':
            return self._handleOptions(view, kwargs)
        else:
            if method not in view.allowedMethods:
                #Returns 405 response if request method is not in the view's allowed methods
                return self._405MethodNotAllowed(view.allowedMethods)

            return view.view(self.request, **kwargs)

    def getErrorHandlerResponse(self, response=None, statusCode=None):
        #Goes through all the errorHandlers
        for handler in self.errorHandlers:
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

    def _405MethodNotAllowed(self, allowedMethods) -> HTTPResponse:
        '''Returns a 405 response'''
        response = self.getErrorHandlerResponse(statusCode=405)
        
        methods = ', '.join(allowedMethods)
        if self.debug:
            if response == None:
                render = renderErrorPage(
                    mainMessage='405 Method Not Allowed',
                    subMessage=f'Allowed Methods: {methods}',
                )
                res = HTTPResponse(content=render, status=405) 
                res.headers['Allow'] = methods
                return res
            else:
                return response
        else:
            if response == None:
                res = HTTPResponse(content='405 Method not Allowed', status=405) 
                res.headers['Allow'] = methods
                return res
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
                view, kwargs = self.findView()
                if view.unstripedPath.endswith('/') == False and root.endswith('/'):
                    raise HTTP404

                #if the view path ends with a slash and the client goes to that page without a slash redirect to page without slash
                elif view.unstripedPath.endswith('/') and root.endswith('/') == False:
                    #Gets the url params and adds them to the redirected url
                    paramsSplit = self.request.path.split('?')
                    params = (f'?{"?".join(paramsSplit[1:])}' if len(paramsSplit) >= 2 else '')
                    return HTTPResponsePermenentRedirect(f'{root}/{params}')

                #This runs the view function, and gets the response.
                response = self._handleMethod(self.request.method, view, kwargs)

                #If error handler doesnt exist for the status code of the response, then this returns the response given.
                response = self.getErrorHandlerResponse(response)
                return response
                
            except HTTP404:
                errorHandlerRequest = self.getErrorHandlerResponse(statusCode=404)
                return pageNotFound(errorHandlerRequest, self.debug, self.views)
        else:
            try:
                return getStaticFileResponse(self.request, root, ext)
            except HTTP404:
                errorHandlerRequest = self.getErrorHandlerResponse(statusCode=404)
                return pageNotFound(errorHandlerRequest, self.debug, self.views)
                
