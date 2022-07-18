import importlib
import waffleweb

from waffleweb.request import Request, RequestHandler
from waffleweb.exceptions import MiddlewareNotFoundError, MiddlewareImportError

class Middleware:
    '''
    This is a special list for storing middleware. 
    
    It has special abilities that load middleware when middleware is appended or replaced.
    '''
    
    def __init__(self, middleware: list[str] = []):
        self.middleware = []
        for ware in middleware:
            self.middleware.append(self.loadMiddleware(ware))
    
    def loadMiddleware(self, ware):
        """Loads a middleware string."""
        
        #Trys to import middleware, if can't, raise MiddlewareNotFoundError
        try:
            #Gets the module and the middleware name
            splitMiddlewareName = ware.split('.')
            if len(splitMiddlewareName) < 2:
                raise MiddlewareImportError('Your middleware has to have a module and a class that is the middleware, example: moduleName.middlewareClass')
            
            #Gets the variable
            ware = splitMiddlewareName[len(splitMiddlewareName) - 1]

            #Gets the module
            module = ".".join(splitMiddlewareName[:(len(splitMiddlewareName) - 1)]) 
        
            #Imports the middleware
            module = importlib.import_module(module)

            #Adds it to the middleware list
            loadedMiddleware = {
                'module': module,
                'middleware': getattr(module, str(ware))
            }
        except ModuleNotFoundError:
            raise MiddlewareNotFoundError(f'Could not find middleware "{str(ware)}"')

        return loadedMiddleware

    def append(self, middleware: str):
        if type(middleware) == str:
            return self.middleware.append(self.loadMiddleware(middleware))
        elif type(middleware) == list:
            for ware in middleware:
                return self.middleware.append(self.loadMiddleware(ware))
        else:
            raise TypeError('The middleware has to be a str or a list.')
            
    def clear(self):
        return self.middleware.clear()
        
    def copy(self):
        return self.middleware.copy()
        
    def count(self, value):
        return self.middleware.count(value)
        
    def extend(self, middleware):
        for ware in middleware:
            self.middleware.append(self.loadMiddleware(ware))
            
    def index(self, value):
        return self.middleware.index(value)
        
    def insert(self, index: int, middleware: str):
        return self.middleware.insert(index, self.loadMiddleware(middleware))
        
    def pop(self, index: int):
        return self.middleware.pop(index)

    def remove(self, value):
        return self.middleware.remove(value)            

    def reverse(self):
        return self.middleware.reverse()
        
    def sort(self, reverse=False, key=None):
        return self.middleware.sort(reverse, key)
        
    def __str__(self) -> str:
        return str(self.middleware)
        
    def __repr__(self) -> str:
        return repr(self.middleware)
        
    def __setitem__(self, index, newvalue):
        self.middleware[index] = self.loadMiddleware(newvalue)
        
    def __getitem__(self, index):
        return self.middleware[index]

class MiddlewareHandler():
    def __init__(self, middleware: Middleware):
        #Gets the middleware
        self.middleware = middleware

    def runRequestMiddleware(self, request: Request) -> Request:
        '''Runs all the middleware on the request'''

        for ware in self.middleware:
            ware = ware['middleware']

            #Trys to run the middleware's before function
            try:
                newRequest = ware.before(request)

                #Makes sure middleware returns Request object.
                if type(newRequest) == Request:
                    request = newRequest
            except AttributeError:
                pass

        return request

    def runResponseMiddleware(self, response):
        '''Runs all the middleware on the response'''
        
        for ware in self.middleware:
            ware = ware['middleware']

            #Trys to run the middleware's after function
            try:
                response = ware.after(response)
            except AttributeError:
                pass
        
        return response
