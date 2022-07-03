import os
import socket
import ipaddress
import datetime
import importlib
import traceback
import waffleweb

try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None

from waffleweb.response import HTTPResponse, HTTP404
from waffleweb.request import Request, RequestHandler
from waffleweb.template import renderErrorPage, renderTemplate
from waffleweb.middleware import MiddlewareHandler
from waffleweb.wsgi import WsgiHandler
from waffleweb.exceptions import AppNotFoundError, AppImportError, ParsingError
from waffleweb.errorResponses import badRequest

class WaffleProject():
    '''
    The centre of all waffleweb projects. It takes two arguments: 
        apps - list of string - Apps hold all of your views, they can be a single python 
        file or a folder. Each app in your list has to be 
        as so: moduleName.waffleAppObject

        middleware - list of string - this is list of all your middleware,
        Each middleware in your list has to be as so: moduleName.middlewareObject
    '''

    def __init__(self, apps: list[str], middleware: list[str]=[]):
        self.apps = self.loadApps(apps)
        waffleweb.defaults.APPS = self.apps
        self.middlewareHandler = MiddlewareHandler(middleware)

    def loadApps(self, apps: list[str]) -> list:
        '''
        This function looks for and imports all the apps and adds them to a 
        dictionary then adds it to a list then returns the list.
        '''

        loadedApps = []

        for app in apps:
            #trys to import app, if can't, raise AppNotFoundError
            try:
                #Gets the module and the app name
                splitAppName = app.split('.')
                if len(splitAppName) < 2:
                    raise AppImportError('Your app has to have a module and a WaffleApp, example: moduleName.waffleAppObjectName')

                #Gets the a varible
                app = splitAppName[len(splitAppName) - 1]

                #Gets the module
                module = ".".join(splitAppName[:(len(splitAppName) - 1)])

                #imports the app
                module = importlib.import_module(module)

                #adds it to app list
                loadedApps.append({
                                'module': module,
                                'app': getattr(module, str(app)),
                    }) 
            except ModuleNotFoundError:
                raise AppNotFoundError(f'Could not find app "{str(app)}"')
        
        return loadedApps

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
            if 1 > port or port > 65535:
                raise ValueError('port has to be more 1 and less that 65536!')
        except:
            raise TypeError('port has to be a int!')

        #Starts the test server socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)

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
                        handler = RequestHandler(request, debug)

                        view = None
                        try:
                            #Run middleware on Request
                            view = handler.getView()[0]
                            request = self.middlewareHandler.runRequestMiddleware(request, view)
                            handler.request = request
                        except HTTP404:
                            pass
                        
                        #gets the response
                        response = handler.getResponse()

                        if view is not None:
                            #Run middleware on response
                            response = self.middlewareHandler.runResponseMiddleware(response, view)
                            
                        #sends the response
                        conn.sendall(bytes(response))

                        #prints the request information
                        timeNow = datetime.datetime.now()
                        print(f'[{timeNow.strftime("%m/%d/%Y %H:%M:%S")}] {handler.request.HTTPVersion} {handler.request.method} {handler.request.path} {response.statusCode} {response.reasonPhrase}')

                        #closes the connection
                        conn.close()
                    except ParsingError:
                        return bytes(badRequest(self.apps, debug))
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
                            conn.sendall(bytes(HTTPResponse(content='<h1>An error occured!</h1>', status=500)))

            except KeyboardInterrupt as e:
                print('\nKeyboardInterrupt, Closing server')
                return

    def wsgiApplication(self, environ, startResponse):
        handler = WsgiHandler(environ, self.apps, self.middlewareHandler)
        
        #Gets the response
        handler.getResponse()
        
        #Gets the data
        content = handler.getResponseContent()
        headers = handler.getResponseHeaders()
        status = handler.getResponseStatus()

        startResponse(status, headers)
        return iter([content])