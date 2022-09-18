import waffleweb
import socket
import ipaddress
import datetime
import traceback

from waffleweb.middleware import runResponseMiddleware, runRequestMiddleware
from waffleweb.request import Request, getResponse
from waffleweb.response import HTTPResponse
from waffleweb.exceptions import ParsingError
from waffleweb.errorResponses import BadRequest, InternalServerError

class WaffleServer:
    '''
    This is a webserver made to be easily customizable. This webserver
    should not be used in production as it does not have proper 
    security. 
    
    Parameters:
    - getResponseFunc - The function that gets the 
    response to return to the client. Your function should take a 
    ``Request`` object if raw is False, but if ``raw`` is True, the 
    function  should take a ``bytes`` string. Your function should also
    take a ``debug`` parameter. ``getResponseFunc`` is called whenever
    a request comes in.
    
    - ``raw`` (``bool``) - This parameter dictates if a ``bytes`` 
    string or a ``Request`` object is passed to the ``getResponseFunc``.
    
    - ``runMiddleware`` (``bool``) - If the middleware should be run on 
    the request and the response. If ``raw`` and is on then middleware 
    won't be run on requests.
    '''
    
    def __init__(self, getResponseFunc, raw=False, runMiddleware=True):
        self.getResponseFunc = getResponseFunc
        self.raw = raw
        self.runMiddleware = runMiddleware
    
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
            
            print(f'Waffleweb version {waffleweb.__version__}')
            print(f'Server listening on host {host}, port {port}')
            print(f'Press Ctrl+C to stop server')
            try:
                while True:
                    try:
                        #waits for connection to server
                        conn, addr = sock.accept()

                        #Gets the request
                        req = conn.recv(2048)
                        
                        if self.raw == False:
                            try:
                                #Turns the request into a Request object.
                                request = Request(req, addr)
                            except ParsingError:
                                response = BadRequest(debug=debug)
                                
                                #prints the request information
                                timeNow = datetime.datetime.now()
                                print(f'[{timeNow.strftime("%m/%d/%Y %H:%M:%S")}] Unknown Unknown Unknown {response.statusCode} {response.reasonPhrase}')
                                conn.sendall(bytes(response))
                                conn.close()
                                continue
                        else:
                            request = req

                        if self.raw == False or self.runMiddleware:
                            #Runs middleware on request
                            request = runRequestMiddleware(request, waffleweb.currentWorkingApp.middleware)
                        
                        #gets the response
                        response = self.getResponseFunc(request, debug)

                        if self.runMiddleware:
                            #Run middleware on response
                            response = runResponseMiddleware(response, waffleweb.currentWorkingApp.middleware)

                    except Exception as e:
                        #prints the exception
                        traceback.print_exc()

                        #if debug mode is on return a page with the error data, else give generic error
                        response = InternalServerError(e, debug=debug)
                    
                    #prints the request information
                    timeNow = datetime.datetime.now()
                    print(f'[{timeNow.strftime("%m/%d/%Y %H:%M:%S")}] {request.HTTPVersion} {request.method} {request.path} {response.statusCode} {response.reasonPhrase}')
                    
                    #Adds the Server header to the response
                    response.headers["Server"] = "Waffleweb Server"
                    
                    conn.sendall(bytes(response))
                    conn.close()   

            except KeyboardInterrupt as e:
                print('\nKeyboardInterrupt, Closing server')
                return
                