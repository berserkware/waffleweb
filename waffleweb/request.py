import os
import importlib
import waffleweb
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from urllib.parse import urlparse, unquote
from waffleweb.errorResponses import methodNotAllowed, pageNotFound
from waffleweb.cookie import Cookies
from waffleweb.response import HTTP404, FileResponse, HTTPResponse, HTTPResponsePermenentRedirect, JSONResponse
from waffleweb.static import getStaticFileResponse
from waffleweb.parser import parseBody, parseHeaders, parsePost, splitURL, parseURLParameters
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

        self.URL_PARAMS = self.URL_PARAMS | parseURLParameters(self.path)
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

    def _matchPartInView(self, index, part) -> tuple:
        '''This is used to match a part in a requested URL, to a URL variable in a view. It also converts the variable to the type.'''
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

    def findView(self):
        '''Finds a view matching the request url, Returns the view function and the views kwargs.'''

        self.root, self.splitRoot, self.ext = splitURL(self.request.path)
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
                            kwarg = self._matchPartInView(index, part)
                            viewKwargs[kwarg[0]] = kwarg[1]

                if urlMatches:
                    return (view, viewKwargs)
    
        raise HTTP404

    def _handleHead(self, view, kwargs):
        #Checks if GET or HEAD is in allowed methods
        if 'GET' not in view.allowedMethods and 'HEAD' not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            res = self.getErrorHandlerResponse(statusCode=405)
            return methodNotAllowed(res, self.debug, view.allowedMethods)

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
            res = self.getErrorHandlerResponse(statusCode=405)
            return methodNotAllowed(res, self.debug, view.allowedMethods)

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

    def _handleOther(self, view, kwargs, method):
        if method not in view.allowedMethods:
            #Returns 405 response if request method is not in the view's allowed methods
            res = self.getErrorHandlerResponse(statusCode=405)
            return methodNotAllowed(res, self.debug, view.allowedMethods)

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

    def getResponse(self):
        '''Gets a response to a request, retuerns Response.'''

        root, splitRoot, ext = splitURL(self.request.path)
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
               
                #Matches the method to its function.
                if self.request.method == 'HEAD':
                    response = self._handleHead(view, kwargs)
                elif self.request.method == 'OPTIONS':
                    response = self._handleOptions(view, kwargs)
                else:
                    response = self._handleOther(view, kwargs, self.request.method)

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
                
