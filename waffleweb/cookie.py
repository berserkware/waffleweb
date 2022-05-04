class Cookie():
    '''This is a cookie num num num'''

    def __init__(self, name, value, path='/'):
        self.name = str(name)
        self.value = value
        self.path = path

    def __str__(self):
        return f'{self.name}={self.value}; path={self.path}'

class Cookies(dict):
    '''This stores Cookies, it is a dictionary.'''

    def __init__(self, cookies=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if cookies is not None:
            for cookie in cookies.split(';'):
                name, value = cookie.split('=')
                self[str(name).strip()] = Cookie(name, value, '/')

    def __str__(self):
        cookies = []
        for cookieKey in self.keys():
            cookie = f'{cookieKey}={self[cookieKey].value}'
            cookies.append(cookie)

        cookiess = '; '.join(cookies)
        if cookiess != '':
            return '; '.join(cookies)
        else:
            return ''

    def setCookie(self, name, value, path):
        '''Sets a cookie to a value, takes two arguments: name and value.'''
        self[str(name)] = Cookie(name, value, path)

    def removeCookie(self, name):
        '''Deletes a cookie if exists, takes one argument: name.'''
        if str(name) in self.keys():
            del self[str(name)]
        else:
            raise ValueError('You can\'t remove a cookie that doesn\'t exist!')