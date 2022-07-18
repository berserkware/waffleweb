import unittest

from waffleweb import WaffleApp
from waffleweb.request import Request
from waffleweb.response import HTTPResponse
from waffleweb.cookie import Cookies

class basicCookieTest(unittest.TestCase):
    def test_cookie(self):
        app = WaffleApp()
        
        @app.route('/cookieTest')
        def cookieTest(request):
            res = HTTPResponse(request, content='testing 123')
            res.setCookie('testCookie', 'testVal')
            return res
            
        response = app.request(b'GET /cookieTest HTTP/1.1\r\n\r\n')
    
        self.assertEqual(str(response.headers['Set-Cookie']), 'testCookie=testVal; path=/cookieTest; SameSite=Lax')

class CookiesTest(unittest.TestCase):
    def test_getCookie(self):
        cookies = Cookies('testCookie=testValue; testCookie2=testCookie2')
        self.assertEqual(cookies['testCookie'].value, 'testValue')
        self.assertEqual(cookies['testCookie2'].value, 'testCookie2')

    def test_strCookie(self):
        cookies = Cookies('testCookie=testValue; testCookie2=testValue2')
        self.assertEqual(str(cookies), 'testCookie=testValue; testCookie2=testValue2')