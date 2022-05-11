import socket
import ipaddress
import datetime
import importlib
import traceback
import waffleweb

from waffleweb.response import HTTPResponse, HTTP404
from waffleweb.request import Request, RequestHandler
from waffleweb.template import renderErrorPage, renderTemplate

class AppNotFoundError(Exception):
    pass

class WaffleProject():
    '''
    The centre of all waffleweb projects. It takes only one
    argument: apps. Apps hold all of your views, they can be 
    a single python file or a folder.
    '''

    def __init__(self, apps: list):
        self.apps = []

        self._importApps(apps)

    def _importApps(self, apps):
        '''This function looks for and imports all the app and adds them to a dictionary.'''

        for app in apps:
            #checks if appname ends with a python file extension
            if app.endswith(('.py', '.py3')):
                #checks if can import app, if can't raises eception
                try:
                    module = importlib.import_module(app[:app.index(".")])
                    self.apps.append({
                                    'module': module,
                                    'app': module.app,
                    }) 
                except ModuleNotFoundError:
                    raise AppNotFoundError(f'Could not find app "{app[:app.index(".")]}"')
            else:
                #checks if can import folder app, if can't raise exception
                try:
                    importlib.import_module(f"{app}.{app}")
                    module = importlib.import_module(app)
                    self.apps.append({
                        'module': module,
                        'app': module.app,
                    })
                except ModuleNotFoundError:
                    raise AppNotFoundError(f'Could not find app "{app}", make sure you spelled it right and you app has a "{app}.py" file in it')

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

                        #turns the request into a Request object.
                        request = Request(conn.recv(1024).decode(), addr)

                        #Creates a RequestHandler object.
                        handler = RequestHandler(request, self.apps, debug)

                        #gets the response
                        response = handler.getResponse()

                        #sends the response
                        conn.sendall(bytes(response))

                        #prints the request information
                        timeNow = datetime.datetime.now()
                        print(f'[{timeNow.strftime("%m/%d/%Y %H:%M:%S")}] {handler.request.HTTPVersion} {handler.request.method} {handler.request.path} {response.statusCode} {response.reasonPhrase}')

                        #closes the connection
                        conn.close()
                    except Exception as e:
                        #gets the exception
                        exception = traceback.TracebackException.from_exception(e)
                        
                        #prints the excepts
                        traceback.print_exc()

                        #if debug mode is on return a page with the error data else give generic error
                        if debug:
                            #gets the traceback
                            stack = exception.stack.format()
                            stackStr = '\n'.join([f'<code>{stackLine}</code>' for stackLine in stack])

                            context = {
                                'mainErrorMessage': exception.exc_type.__name__,
                                'subErrorMessage': str(e),
                                'trackbackMessage': stackStr,
                                }

                            response = HTTPResponse(None, renderErrorPage(context['mainErrorMessage'], context['subErrorMessage'], context['trackbackMessage']))
                            conn.sendall(bytes(response))
                        else:
                            conn.sendall(bytes(HTTPResponse(None, '<h1>An error occured!</h1>')))

            except KeyboardInterrupt as e:
                print('\nKeyboardInterrupt, Closing server')
                return

