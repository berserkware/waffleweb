import unittest

from waffleweb.cookie import Cookie, Cookies

class CookieTest(unittest.TestCase):
    def test_cookieStrDefault(self):
        cookie = Cookie('name', 'value')
        self.assertEqual(str(cookie), 'name=value; SameSite=Lax')
        
    def test_cookieStrWithPath(self):
        cookie = Cookie('name', 'value', '/test')
        self.assertEqual(str(cookie), 'name=value; path=/test; SameSite=Lax')
        
    def test_cookieStrWithMaxAge(self):
        cookie = Cookie('name', 'value', maxAge='max')
        self.assertEqual(str(cookie), 'name=value; Max-Age=max; SameSite=Lax')
        
    def test_cookieStrWithDomain(self):
        cookie = Cookie('name', 'value', domain='domain')
        self.assertEqual(str(cookie), 'name=value; Domain=domain; SameSite=Lax')
    
    def test_cookieStrWithSecure(self):
        cookie = Cookie('name', 'value', secure=True)
        self.assertEqual(str(cookie), 'name=value; Secure; SameSite=Lax')
        
    def test_cookieStrWithHTTPOnly(self):
        cookie = Cookie('name', 'value', HTTPOnly=True)
        self.assertEqual(str(cookie), 'name=value; HttpOnly; SameSite=Lax')
        
class CookiesTest(unittest.TestCase):
    def test_getCookieSingle(self):
        cookies = Cookies('testCookie=testValue')
        self.assertEqual(cookies['testCookie'].value, 'testValue')
    
    def test_getCookieMultiple(self):
        cookies = Cookies('testCookie=testValue; testCookie2=testCookie2')
        self.assertEqual(cookies['testCookie'].value, 'testValue')
        self.assertEqual(cookies['testCookie2'].value, 'testCookie2')

    def test_strCookie(self):
        cookies = Cookies('testCookie=testValue; testCookie2=testValue2')
        self.assertEqual(str(cookies), 'testCookie=testValue; testCookie2=testValue2')