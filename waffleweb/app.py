import re

class waffleApp():
    def __init__(self, appName):
        self.appName = appName
        self.views = []

    def route(self, path, name):
        '''
        This is the decorator you put on all your views it gives your view a URL and a name.
        It takes two arguments path and name. The path argument is the reletive URL to your 
        view and the name argument is the name of your view.

        the name argument is used to reference the view in templates and redirects, it looks
        like this: appName:name

        You can add varibles to your url by puting <argumentName:valueType>
        you then add the argumentName to your views arguments, example:

        @app.route('profile/<username:str>')
        def profileView(request, username):
            #your view logic goes here

        '''
        
        def decorator(view):
            print('dec')
            def wrapper(*args, **kwargs):
                print('wrap')
                #regex from https://stackoverflow.com/questions/31430167/regex-check-if-given-string-is-relative-url
                if re.compile(r'^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*').search(path):
                    view(*args, **kwargs)
                else:
                    raise ValueError('Your path has to be a valid reletive URL pattern.')
            return wrapper
        return decorator

app = waffleApp('mainPage')

@app.route('index/', 'index')
def index(request=None):
    pass