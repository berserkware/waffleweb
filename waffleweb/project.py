import socket
import ipaddress
import datetime
import importlib
import os

import waffleweb
from waffleweb.request import Request
from waffleweb.response import HTTPResponse, HTTP404

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
    
    def handleRequest(self, request: Request):
        '''Handles the HTTP request.'''

        #gets the root and file extenstion
        root, ext = os.path.splitext(request.path)
        root = root.strip('/')
        splitRoot = root.split('/')

        if ext == '':
            #Searches through all the apps to match the url
            for app in self.apps:
                module = app['module']
                app = app['app']

                for view in app.views:
                    urlMatches = True
                    viewKwargs = {}

                    if view['path'] == root:
                        return view['view'](request)

                    if len(view['splitPath']) == len(splitRoot) and view['splitPath'] != ['']:
                        for index, part in enumerate(view['splitPath']):
                            if part != splitRoot[index] and type(part) == str:
                                urlMatches = False
                                break
                            
                            if type(part) == list:
                                viewKwargs[str(part[0])] = splitRoot[index]

                        if urlMatches:
                            return view['view'](request, **viewKwargs)
        else:
            pass
        #Returns 404 if doesn't match URL
        raise HTTP404

    def run(self, host='127.0.0.1', port=8000):
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
                    #waits for connection to server
                    conn, addr = sock.accept()

                    #turns the request into Request class
                    req = Request(conn.recv(1024).decode(), addr)

                    #gets the response
                    try:
                        response = self.handleRequest(req)
                    except HTTP404:
                        response = HTTPResponse('The requested page could not be found', status=404)

                    #sends the response
                    conn.sendall(bytes(response))

                    timeNow = datetime.datetime.now()
                    print(f'[{timeNow.strftime("%m/%d/%Y %H:%M:%S")}] HTTP/1.1 {req.method} {req.path} {response.statusCode} {response.reasonPhrase}')

                    #closes the connection
                    conn.close()
            except KeyboardInterrupt as e:
                print('\nKeyboardInterrupt, Closing server')
                return
