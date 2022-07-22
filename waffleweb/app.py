import re
import os
import socket
import ipaddress
import datetime
import traceback
import waffleweb

from waffleweb.middleware import MiddlewareHandler, Middleware
from waffleweb.request import Request, RequestHandler
from waffleweb.response import HTTP404, HTTPResponse
from waffleweb.exceptions import ParsingError
from waffleweb.errorResponses import badRequest
from waffleweb.template import renderErrorPage
from waffleweb.wsgi import WsgiHandler
from waffleweb.datatypes import MultiValueOneKeyDict

class View:
    '''A view.'''
    def __init__(
        self,
        unstripedPath=None,
        path=None,
        splitPath=None,
        name=None,
        view=None,
        allowedMethods=None,
        ):
        self.unstripedPath = unstripedPath
        self.path = path
        self.splitPath = splitPath
        self.name = name
        self.view = view
        self.allowedMethods = allowedMethods
        
    def hasPathHasArgs(self) -> bool:
        for part in self.splitPath:
            if type(part) == list:
                return True
        return False
        
class ErrorHandler:
    def __init__(
        self,
        statusCode,
        view,
        ):
        self.statusCode = statusCode
        self.view = view

class WaffleApp():
    '''
    The WaffleApp() class is the center of your website.
    app = WaffleApp('yourAppName')
    '''

    def __init__(self):
        self.middleware = Middleware()
        self.views = []
        self.errorHandlers = []

    def route(self, path='/', name=None, methods=['GET']):
        '''
        This is the decorator you put on all your views it gives your view a URL and a name.
        It takes two arguments path and name. The path argument is the relative URL to your 
        view and the name argument is the name of your view.

        the name argument is defaulted to the name of your view function. it is used to reference 
        the view in templates and redirects, it looks like this: appName:name

        You can add variables to your url by puting <argumentName:valueType>
        you then add the argumentName to your views arguments.

        You can make a view only allowed certain methods by adding a list to your view decorator.
        It defaults to all HTTP/1.1 methods

        View example:

        @app.route('profile/<username:str>', 'profile', methods=['GET', 'POST'])
        def profileView(request, username):
            #your view logic goes here
        '''

        def decorator(view):
            #regex from https://stackoverflow.com/questions/31430167/regex-check-if-given-string-is-relative-url
            #this checks to see if the URL is relative
            if re.compile(r'^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*').search(path):
                splitPathWithArgs = []
                splitPath = str(path).strip('/').split('/')

                for part in splitPath:
                    if part != '':
                        #checks if part is a URL argument
                        if part[0] == '<' and part[-1] == '>':
                            #gets the arg without the < and >
                            partArg = part[1:-1]

                            #splits Args into name and type
                            argList = partArg.split(':')

                            #checks if argument has name and type
                            if len(argList) != 2:
                                raise AttributeError('Your URL arguments have to have a name and a type')

                            if argList[1] not in ['int', 'str', 'float']:
                                raise AttributeError('Your URL argument type has to be a int, str or float')
                            
                            splitPathWithArgs.append(argList)
                        else:
                            splitPathWithArgs.append(part)
                
                #adds function to view registry
                self.views.append(
                    View(
                    unstripedPath=path,
                    path=path.strip('/'),
                    splitPath=splitPathWithArgs,
                    name=(view.__name__ if name == None else name),
                    view=view,
                    allowedMethods=methods,
                    ))

                def wrapper(*args, **kwargs):
                    return view(*args, **kwargs)

                return wrapper
            else:
                raise ValueError('Your path has to be a valid relative URL pattern.')
        return decorator
        
    def errorHandler(self, statusCode: int):
        def decorator(view):
            #Checks if status code is valid.
            if statusCode is not None:
                try:
                    self.statusCode = int(statusCode)
                except(ValueError, TypeError):
                    raise TypeError('HTTP status code has to be an integer.')

                if 100 > statusCode or statusCode > 599:
                    raise ValueError('HTTP status code must be a integer from 100 to 599.')
                    
            self.errorHandlers.append(
                ErrorHandler(statusCode, view)
            )
            def wrapper(*args, **kwargs):
                return view(*args, **kwargs)
                
            return wrapper
        return decorator
        
    def request(self, rawRequest: bytes):
        '''Sends a request to any of the views.'''
        
        request = Request(rawRequest, '127.0.0.1')
        handler = RequestHandler(request, debug=False, app=self)
        
        middlewareHandler = MiddlewareHandler(self.middleware)
        
        request = middlewareHandler.runRequestMiddleware(request)
        
        #gets the response
        response = handler.getResponse()

        response = middlewareHandler.runResponseMiddleware(response)
            
        return response
        
    def run(self, host='127.0.0.1', port=8000, debug=False):
        '''
        This runs the test server,
        default host is 127.0.0.1,
        default port is 8000.
        Note: don't use this in production
        '''

        #Checks if host is valid
        try:
            ipaddress.ip_address(host)
        except ValueError:
            raise ValueError('host is invalid!')

        #Checks if port is valid
        try:
            port = int(port)
        except ValueError:
            raise TypeError('port has to be a int!')
            
        if 1 > port or port > 65535:
            raise ValueError('port has to be more 1 and less that 65536!')

        #Starts the test server socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)
            
            middlewareHandler = MiddlewareHandler(self.middleware)

            print(f'Waffleweb version {waffleweb.__version__}')
            print(f'Server listening on host {host}, port {port}')
            print(f'Press Ctrl+C to stop server')
            try:
                while True:
                    try:
                        #waits for connection to server
                        conn, addr = sock.accept()

                        req = conn.recv(2048)
                        
                        #turns the request into a Request object.
                        request = Request(req, addr)

                        #Creates a RequestHandler object.
                        handler = RequestHandler(request, debug, self)

                        request = middlewareHandler.runRequestMiddleware(request)
                        
                        #gets the response
                        response = handler.getResponse()

                        #Run middleware on response
                        response = middlewareHandler.runResponseMiddleware(response)
                            
                        #sends the response
                        conn.sendall(bytes(response))

                        #prints the request information
                        timeNow = datetime.datetime.now()
                        print(f'[{timeNow.strftime("%m/%d/%Y %H:%M:%S")}] {handler.request.HTTPVersion} {handler.request.method} {handler.request.path} {response.statusCode} {response.reasonPhrase}')

                        #closes the connection
                        conn.close()
                    except ParsingError:
                        return bytes(badRequest(self, debug))
                    except Exception as e:
                        #gets the exception
                        exception = traceback.TracebackException.from_exception(e)
                        
                        #prints the excepts
                        traceback.print_exc()

                        #if debug mode is on return a page with the error data else give generic error
                        if debug:
                            splitTraceback = []
                            #gets the traceback
                            stack = exception.stack.format()
                            for stackLine in stack:
                                stackLines = []
                                
                                splitStackLine = stackLine.split(', ')
                                file = splitStackLine[0]
                                lineNumber = splitStackLine[1]
                                code = splitStackLine[2].strip('\n')
                                
                                #Gets the filePath line
                                filePath = file.strip().split(' ')[1].strip('"')
                                func = code.split(' ')[1].strip('\n').strip()
                                stackLines.append(f'{filePath} in {func}():')

                                #Gets the code line
                                lineNumber = lineNumber.split(' ')[1]
                                code = stackLine.split('\n')[1]

                                stackLines.append(f'{lineNumber}: {code}')

                                splitTraceback.append(f'<code>{stackLines[0]}</code><br><div style="width: 100%; background-color: #d1d1d1;"><code style="margin-left: 15px; margin-top: 0px; margin-bottom: 0px;">{stackLines[1]}</code></div><br>')


                            stackStr = '\n'.join(splitTraceback)

                            context = {
                                'mainErrorMessage': exception.exc_type.__name__,
                                'subErrorMessage': str(e),
                                'trackbackMessage': stackStr,
                                }

                            response = HTTPResponse(content=renderErrorPage(context['mainErrorMessage'], context['subErrorMessage'], context['trackbackMessage']), status=500)
                            conn.sendall(bytes(response))
                        else:
                            conn.sendall(bytes(HTTPResponse(content='<title>500 Internal Server Error</title><h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">500</h1><h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">Internal Server Error.</h3>', status=500)))

            except KeyboardInterrupt as e:
                print('\nKeyboardInterrupt, Closing server')
                return
                
    def wsgiApplication(self, environ, startResponse):
        middlewareHandler = MiddlewareHandler(self.middleware)
        handler = WsgiHandler(MultiValueOneKeyDict(environ), self, middlewareHandler)
        
        #Gets the response
        handler.getResponse()
        
        #Gets the data
        content = handler.getResponseContent()
        headers = handler.getResponseHeaders()
        status = handler.getResponseStatus()

        startResponse(status, headers)
        return iter([content])
                
app = WaffleApp()