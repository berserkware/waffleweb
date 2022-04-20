import socket
import ipaddress
import datetime
import importlib
import traceback

import waffleweb
from waffleweb.request import Request
from waffleweb.exceptions import AppNotFoundError

class WaffleProject():
    '''
    The centre of all waffleweb projects. It takes only one
    argument: apps. Apps hold all of your views, they can be 
    a single python file or a folder.
    '''

    def __init__(self, apps: list, BASE_DIR=None):
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
        path = request.path.strip('/')

        #Searches through all the apps to match the url
        for app in self.apps:
            module = app['module']
            app = app['app']
            for view in app.views:
                if view['path'].strip('/') == path:
                    return view['view'](request)

        #Returns 404 if doesn't match URL
        return b"HTTP/1.1 404 NOT FOUND\n\nThe requested page could not be found"

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
                    response = self.handleRequest(req)

                    #sends the response
                    conn.sendall(bytes(response))

                    timeNow = datetime.datetime.now()
                    print(f'{req.method} [{timeNow.strftime("%m/%d/%Y  %H:%M:%S")}] {req.path}')

                    #closes the connection
                    conn.close()
            except KeyboardInterrupt as e:
                print('\nKeyboardInterrupt, Closing server')
                return
