import re

class waffleApp():
    def __init__(self, appName):
        self.appName = appName

    def route(self, path, name):
        def decorator(view):
            def wrapper(*args, **kwargs):
                if re.compile(r'^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*').search(path):
                    view(*args, **kwargs)
                else:
                    raise ValueError('Your path has to be a valid reletive URL pattern.')
            return wrapper
        return decorator

app = waffleApp('mainPage')