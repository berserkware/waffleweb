import re

class WaffleApp():
    '''
    The WaffleApp() class is the centre of all the apps for your project.
    It only takes one argument: name, which is the name of your
    application. It is automatically defined when you create an app as so: 
    app = WaffleApp('yourAppName')
    '''

    def __init__(self, appName: str):
        self.appName = appName
        self._views = []

    @property
    def views(self):
        return self._views

    def route(self, path: str, name=None):
        '''
        This is the decorator you put on all your views it gives your view a URL and a name.
        It takes two arguments path and name. The path argument is the reletive URL to your 
        view and the name argument is the name of your view.

        the name argument is defualted to the name of your view function. it is used to reference 
        the view in templates and redirects, it looks like this: appName:name

        You can add varibles to your url by puting <argumentName:valueType>
        you then add the argumentName to your views arguments, example:

        @app.route('profile/<username:str>', 'profile')
        def profileView(request, username):
            #your view logic goes here

        '''
    
        def decorator(view):
            #regex from https://stackoverflow.com/questions/14549131454913
            #this gets all the attributes in the URLs and removes the <>
            viewURLArgs = re.compile(r'(?<=\<)(.*?)(?=\>)').findall(path)
            viewArgs = []

            #this splits the attributes into their name and type and adds them to a list
            for i in viewURLArgs:
                argList = i.split(':')
                if len(argList) != 2:
                    raise AttributeError('Your URL arguments have to have a name and a type')
                viewArgs.append(argList)

            #regex from https://stackoverflow.com/questions/31430167/regex-check-if-given-string-is-relative-url
            #this checks to see if the URL is reletive
            if re.compile(r'^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*').search(path):
                #adds function to view registry
                if name == None:
                    self._views.append({'path': path, 'name': view.__name__, 'view': view.__name__})
                else:
                    self._views.append({'path': path, 'name': name, 'view': view.__name__})

                def wrapper(*args, **kwargs):
                    #this adds the arguments to the functions arguments
                    for i in viewArgs:
                        kwargs[str(i[0])] = None
                    view(*args, **kwargs)
                return wrapper
            else:
                raise ValueError('Your path has to be a valid relative URL pattern.')
        return decorator