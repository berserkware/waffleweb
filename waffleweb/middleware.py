import importlib
import waffleweb

from waffleweb.request import Request, RequestHandler
from waffleweb.exceptions import MiddlewareNotFoundError, MiddlewareImportError

class MiddlewareHandler():
    def __init__(self, middleware: list[str], apps=None):
        self.middleware = {}
        if apps is None:
            self.apps = waffleweb.defaults.APPS
        else:
            self.apps = apps
        #Gets the global middleware
        self.middleware['global'] = self.loadMiddleware(middleware)

        #Gets the app specific middleware
        for app in self.apps:
            app = app['app']
            self.middleware[app] = self.loadMiddleware(app.middleware)

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
                
                #Gets the variable
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

    def runRequestMiddleware(self, request: Request, app) -> Request:
        '''Runs all the middleware on the request'''

        for ware in self.middleware['global']:
            ware = ware['middleware']

            #Trys to run the middleware's before function
            try:
                newRequest = ware.before(request)

                #Makes sure middleware returns Request object.
                if type(newRequest) == Request:
                    request = newRequest
            except AttributeError:
                pass
        
        #Runs the app specific middleware
        newRew = request
        for ware in self.middleware[app.app]:
            try:
                newRew = ware['middleware'].before(request)

                if type(newRew) == Request:
                    request = newRew
            except (IndexError, AttributeError):
                pass

        return request

    def runResponseMiddleware(self, response, app):
        '''Runs all the middleware on the response'''
        
        for ware in self.middleware['global']:
            ware = ware['middleware']

            #Trys to run the middleware's after function
            try:
                response = ware.after(response)
            except AttributeError:
                pass

        #Runs the app specific middleware
        try:
            for ware in self.middleware[app.app]:
                response = ware['middleware'].after(response)
        except (IndexError, AttributeError):
            pass

        return response
