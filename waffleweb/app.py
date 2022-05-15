import re

from waffleweb.middleware import MiddlewareHandler
from waffleweb.request import Request

class WaffleApp():
    '''
    The WaffleApp() class is the centre of all the apps for your project.
    It only takes one argument: name, which is the name of your
    application. It is automatically defined when you create an app as so: 
    app = WaffleApp('yourAppName')
    '''

    def __init__(self, appName: str, middleware: list[str]=[]):
        self.appName = appName
        self.middlewareHandler = MiddlewareHandler(middleware)
        self._views = []

    @property
    def views(self):
        return self._views

    def route(self, path='/', name=None, methods=['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']):
        '''
        This is the decorator you put on all your views it gives your view a URL and a name.
        It takes two arguments path and name. The path argument is the reletive URL to your 
        view and the name argument is the name of your view.

        the name argument is defualted to the name of your view function. it is used to reference 
        the view in templates and redirects, it looks like this: appName:name

        You can add varibles to your url by puting <argumentName:valueType>
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
            #this checks to see if the URL is reletive
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
                                raise AttributeError('Your URL argument type has to be a integer, string or float')
                            
                            splitPathWithArgs.append(argList)
                        else:
                            splitPathWithArgs.append(part)

                #adds function to view registry
                self._views.append({
                    'unstripedPath': path,
                    'path': path.strip('/'),
                    'splitPath': splitPathWithArgs, 
                    'name': view.__name__ if name == None else name, 
                    'view': view,
                    'allowedMethods': methods,
                    'middlewareHandler': self.middlewareHandler,
                    })

                def wrapper(*args, **kwargs):
                    return view(*args, **kwargs)

                return wrapper
            else:
                raise ValueError('Your path has to be a valid relative URL pattern.')
        return decorator