import os
import importlib
import waffleweb
try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from urllib.parse import urlparse, unquote
from waffleweb.errorResponses import methodNotAllowed, pageNotFound, getErrorHandlerResponse
from waffleweb.cookie import Cookies
from waffleweb.response import HTTP404, FileResponse, HTTPResponse, HTTPResponsePermenentRedirect, JSONResponse
from waffleweb.static import getStaticFileResponse
from waffleweb.parser import parseBody, parseHeaders, parsePost, splitURL, parseURLParameters
from waffleweb.datatypes import MultiValueOneKeyDict
from waffleweb.methodHandler import handleHead, handleOptions, handleOther

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

def matchVariableInURL(indexOfVar, urlVarData, splitUri) -> tuple:
    '''This is used to match a part in a requested URL, to a URL variable in a view. It also converts the variable to the type.'''
    varName = ''
    varValue = None

    #Checks the type of the variable
    if urlVarData[1] == 'int':

        #Gets the name of the variable
        varName = str(urlVarData[0])

        #Converts the value to its type.
        try:
            varValue = int(splitUri[indexOfVar])
        except ValueError:
            varValue = str(splitUri[indexOfVar])

    elif urlVarData[1] == 'float':
        #Gets the name of the variable
        varName = str(urlVarData[0])

        #Converts the value to its type.
        try:
            varValue = float(splitUri[indexOfVar])
        except ValueError:
            varValue = str(splitUri[indexOfVar])

    else:
        #Gets the name of the variable
        varName = str(urlVarData[0])

        #Converts the value to its type.
        varValue = str(splitUri[indexOfVar])

    return (varName, varValue)

def findView(request):
    '''Finds a view matching the requested url, Returns the view function and the views kwargs in a tuple.'''

    uri, splitUri, ext = splitURL(request.path)
    uri = uri.strip('/')

    #Searches through all the views to match the url
    for view in waffleweb.currentRunningApp.views:
        urlMatches = True
        viewKwargs = {}
        #This checks in the path of the view is equal to the reqeusted uri.
        if view.path == uri:
            return (view, {})

        #checks if length of the view's split path is equal to the length of the split request request path
        if len(view.splitPath) == len(splitUri) and view.splitPath != ['']:
            for index, part in enumerate(view.splitPath):
                #checks if path part is equal to the split request path part at the same index
                if part != splitUri[index] and type(part) == str:
                    urlMatches = False
                    break
                
                #makes sure not static file
                if ext == '':
                    #adds variables to view kwargs if part is list
                    if type(part) == list:
                        kwarg = matchVariableInURL(index, part, splitUri)
                        viewKwargs[kwarg[0]] = kwarg[1]

            if urlMatches:
                return (view, viewKwargs)

    raise HTTP404

def getResponse(request, debug: bool=False):
    '''Gets a response to a request, retuerns Response.'''

    app = waffleweb.currentRunningApp

    root, splitRoot, ext = splitURL(request.path)
    try:
        if ext == '':
            #if the route is equal to '*' return a OPTIONS response
            if root == '*':
                return handleOptions(None, {})

            #Gets the view function with its requiured kwargs (url variables)
            view, kwargs = findView(request)

            #If the view path ends without a slash and the client goes to that page with a slash raise 404
            if view.unstripedPath.endswith('/') == False and root.endswith('/'):
                raise HTTP404

            #if the view path ends with a slash and the client goes to that page without a slash redirect to page without slash
            elif view.unstripedPath.endswith('/') and root.endswith('/') == False:
                #Gets the url params and adds them to the redirected url
                paramsSplit = request.path.split('?')
                params = (f'?{"?".join(paramsSplit[1:])}' if len(paramsSplit) >= 2 else '')
                return HTTPResponsePermenentRedirect(f'{root}/{params}')
            
            #Matches the method to its function.
            if request.method == 'HEAD':
                response = handleHead(view, kwargs, request, debug)
            elif request.method == 'OPTIONS':
                response = handleOptions(view, request, debug)
            else:
                response = handleOther(view, kwargs, request, debug)

            #If error handler doesnt exist for the status code of the response, then this returns the response given.
            response = getErrorHandlerResponse(errorHandlers=app.errorHandlers, request=request, response=response)
            return response
        else:
            #If there is a file extention on the url, it will look for a static file, instead of a page.
            return getStaticFileResponse(request, root, ext)
    except HTTP404:
        errorHandlerRequest = getErrorHandlerResponse(errorHandlers=app.errorHandlers, request=request, statusCode=404)
        return pageNotFound(errorHandlerRequest, debug, app.views)
            
