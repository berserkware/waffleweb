import re
import socket
import ipaddress
import datetime
import traceback
import waffleweb

from waffleweb.middleware import runResponseMiddleware, runRequestMiddleware
from waffleweb.request import Request, getResponse
from waffleweb.wsgi import wsgiCallable
from waffleweb.server import WaffleServer

class View:
    '''A view.'''
    def __init__(
        self,
        unstripedPath,
        path,
        splitPath,
        name,
        view,
        allowedMethods,
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
    The WaffleApp class is the core of your site. It is used for routing functions and running the servers.
    '''

    def __init__(self):
        self.views = []
        self.errorHandlers = []
        self.middleware = []
        self.settings = {}

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
            #Checks if status code is valid
            try:
                intStatusCode = int(statusCode)
            except(ValueError, TypeError):
                raise TypeError('HTTP status code has to be an integer.')

            if 100 > intStatusCode or intStatusCode > 599:
                raise ValueError('HTTP status code must be a integer from 100 to 599.')
                    
            self.errorHandlers.append(
                ErrorHandler(intStatusCode, view)
            )

            def wrapper(*args, **kwargs):
                return view(*args, **kwargs)
                
            return wrapper
        return decorator
        
    def request(self, rawRequest: bytes):
        '''Sends a request to any of the views.'''
        
        waffleweb.currentWorkingApp = self

        request = Request(rawRequest, '127.0.0.1')
        
        request = runRequestMiddleware(request, self.middleware)
        
        response = getResponse(request, debug=False)

        response = runResponseMiddleware(response, self.middleware)
            
        return response
        
    def run(self, host='127.0.0.1', port=8000, debug=False):
        '''
        This runs the test server,
        default host is 127.0.0.1,
        default port is 8000.
        Note: don't use this in production
        '''

        waffleweb.currentWorkingApp = self

        server = WaffleServer(getResponse)
        server.run(host, port, debug)
                
    def wsgiApplication(self):
        waffleweb.currentWorkingApp = self

        return wsgiCallable
                
app = WaffleApp()