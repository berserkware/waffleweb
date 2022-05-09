class Cookie():
    '''This is a cookie num num num'''

    def __init__(
            self, 
            name, 
            value, 
            path=None, 
            maxAge=None, 
            domain=None, 
            secure=False, 
            HTTPOnly=False, 
            sameSite=None, 
            strict=False, 
            lax=False, 
            none=False
        ):
        self.name = str(name)
        self.value = value
        self.path = path
        self.maxAge = maxAge
        self.domain = domain
        self.secure = secure
        self.HTTPOnly = HTTPOnly
        self.sameSite = sameSite
        self.strict = strict
        self.lax = lax
        self.none = none

    def __str__(self):
        #returns str for Set-Cookie header
        return f'{self.name}={self.value}; {f"path={self.path}; " if self.path is not None else ""}{f"Domain={self.domain};" if self.domain is not None else ""}{f"Max-Age={self.maxAge};" if self.maxAge is not None else ""}{f"Secure; " if self.secure == True else ""}{f"HttpOnly; " if self.HTTPOnly == True else ""}{f"SameSite={self.sameSite};" if self.sameSite is not None else ""}{f"Strict; " if self.strict == True else ""}{f"Lax; " if self.lax == True else ""}{f"None; " if self.none == True else ""}'

class Cookies(dict):
    '''This stores Cookies, it is a dictionary.'''

    def __init__(self, cookies=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Gets all the cookies from cookies
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

    def setCookie(
            self, 
            name, 
            value, 
            path=None, 
            maxAge=None, 
            domain=None, 
            secure=False, 
            HTTPOnly=False, 
            sameSite=None, 
            strict=False, 
            lax=False, 
            none=False
        ):
        '''Sets a cookie to a value, takes two arguments: name and value.'''
        self[str(name)] = Cookie(name=name, value=value, path=path, maxAge=maxAge, domain=domain, secure=secure, HTTPOnly=HTTPOnly, sameSite=sameSite, strict=strict, lax=lax, none=none)

    def removeCookie(self, name):
        '''Deletes a cookie if exists, takes one argument: name.'''
        if str(name) in self.keys():
            del self[str(name)]
        else:
            raise ValueError('You can\'t remove a cookie that doesn\'t exist!')