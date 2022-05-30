import importlib

from waffleweb.request import Request, RequestHandler
from waffleweb.response import HTTP404

class MiddlewareNotFoundError(Exception):
    pass

class MiddlewareImportError(Exception):
    pass

class MiddlewareHandler():
    def __init__(self, middleware: list[str]):
        self.middleware = self.loadMiddleware(middleware)

    def loadMiddleware(self, middleware: list[str]) -> list:
        '''
        This function looks for and imports all the middleware and adds them to a 
        dictionary then adds it to a list then returns the list.
        '''
        loadedMiddleware = []

        for ware in middleware:
            #Trys to import middleware, if can't, raise MiddlewareNotFoundError
            try:
                #Gets the module and the middleware name
                splitMiddlewareName = ware.split('.')
                if len(splitMiddlewareName) < 2:
                    raise MiddlewareImportError('Your middleware has to have a module and a class that is the middleware, example: moduleName.middlewareClass')
                
                #Gets the varible
                ware = splitMiddlewareName[len(splitMiddlewareName) - 1]

                #Gets the module
                module = ".".join(splitMiddlewareName[:(len(splitMiddlewareName) - 1)]) 
            
                #Imports the middleware
                module = importlib.import_module(module)

                #Adds it to the middleware list
                loadedMiddleware.append({
                    'module': module,
                    'middleware': getattr(module, str(ware))
                })
            except ModuleNotFoundError:
                raise MiddlewareNotFoundError(f'Could not find middleware "{str(ware)}"')

        return loadedMiddleware

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
                else:
                    print(f'Middleware "{ware.__name__}" did not return a Request object, skipping.')
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
