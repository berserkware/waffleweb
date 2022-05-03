class Cookies(dict):
    '''This stores Cookies, it is a dictionary.'''

    def __init__(self, cookies=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if cookies is not None:
            for cookie in cookies.split(';'):
                name, value = cookie.split('=')
                self[str(name).strip()] = str(value).strip()

    def __str__(self):
        cookies = []
        for cookieKey in self.keys():
            cookie = f'{cookieKey}={self[cookieKey]}'
            cookies.append(cookie)

        cookiess = '; '.join(cookies)
        if cookiess != '':
            return '; '.join(cookies)
        else:
            return ''

    def setCookie(self, name, value):
        '''Sets a cookie to a value, takes two arguments: name and value.'''
        self[str(name)] = str(value)

    def removeCookie(self, name):
        '''Deletes a cookie if exists, takes one argument: name.'''
        if str(name) in self.keys():
            del self[str(name)]
        else:
            raise ValueError('You can\'t remove a cookie that doesn\'t exist!')