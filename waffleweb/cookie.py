class Cookie():
    '''
    This is a cookie num num num, takes 11 arguments:
     - name - The name of the cookie.
     - value - The value of the cookie.
     - path - the path of the cookie.
     - maxAge - Maximum age of the cookie.
     - domain - Domian of the cookie.
     - secure - If the cookie is secure
     - HTTPOnly - If the cookie is Http only
     - sameSite - If the cookie is restricted to a first-party or same-site context.
    '''

    def __init__(
            self, 
            name: str, 
            value: str, 
            path: str=None, 
            maxAge: str=None, 
            domain: str=None, 
            secure: bool=False, 
            HTTPOnly: bool=False, 
            sameSite: str='Lax', 
        ):
        self.name = str(name)
        self.value = value
        self.path = path
        self.maxAge = maxAge
        self.domain = domain
        self.secure = secure
        self.HTTPOnly = HTTPOnly
        self.sameSite = sameSite

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        #returns str for Set-Cookie header
        return f'{self.name}={self.value}{f"; path={self.path}" if self.path is not None else ""}{f"; Domain={self.domain}" if self.domain is not None else ""}{f"; Max-Age={self.maxAge}" if self.maxAge is not None else ""}{f"; Secure" if self.secure == True else ""}{f"; HttpOnly" if self.HTTPOnly == True else ""}{f"; SameSite={self.sameSite}" if self.sameSite is not None else ""}'

class Cookies(dict):
    '''
    This stores Cookies, it is a dictionary. Takes 1 arguments:
     - cookies - a string of cookies, example: nameThing=valueThing; anotherNameThing=anotherValueThing
    '''

    def __init__(self, cookies: str=None, *args, **kwargs):
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

        joinedCookies = '; '.join(cookies)

        return joinedCookies