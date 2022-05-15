import unittest

import requests
from waffleweb import WaffleApp
from waffleweb.request import Request
from waffleweb.response import HTTPResponse
from waffleweb.cookie import Cookies

request = Request("""GET /page1/10/index HTTP/1.1
                        Host: localhost:8080
                        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:96.0) Gecko/20100101 Firefox/96.0
                        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
                        Accept-Language: en-US,en;q=0.5
                        Accept-Encoding: gzip, deflate
                        Connection: keep-alive
                        Cookie: csrftoken=Db8QXnkjOLbPd3AGTxlnEEGTSn0IMh44MB8Pf2dVAPSBARoU6DteVUu9nT9ELqcO; sessionid=h8xln73emxlqgpjbsnx9007ceyfla7at
                        Upgrade-Insecure-Requests: 1
                        Sec-Fetch-Dest: document
                        Sec-Fetch-Mode: navigate
                        Sec-Fetch-Site: none
                        Sec-Fetch-User: ?1""", 
                        '101.98.137.19')

class basicCookieTest(unittest.TestCase):
    def test_cookie(self):
        with requests.Session() as s:
            request = s.get('http://localhost:8080/cookieTest')
            self.assertEqual(s.cookies.get_dict(), {'testCookie': 'testVal', 'addedCookie': '32',})

class CookiesTest(unittest.TestCase):
    def test_getCookie(self):
        cookies = Cookies('testCookie=testValue; testCookie2=testCookie2')
        self.assertEqual(cookies['testCookie'].value, 'testValue')
        self.assertEqual(cookies['testCookie2'].value, 'testCookie2')

    def test_strCookie(self):
        cookies = Cookies('testCookie=testValue; testCookie2=testValue2')
        self.assertEqual(str(cookies), 'testCookie=testValue; testCookie2=testValue2')

    def test_setCookie(self):
        cookies = Cookies('testCookie=testValue')
        cookies.setCookie('testCookie2', 'testValue2', '/')
        self.assertEqual(cookies['testCookie2'].value, 'testValue2')
        self.assertEqual(cookies['testCookie'].value, 'testValue')

    def test_removeCookie(self):
        cookies = Cookies('testCookie=testValue; testCookie2=testValue2')
        cookies.removeCookie('testCookie')
        self.assertEqual(str(cookies), 'testCookie2=testValue2')

    def test_removeCookie(self):
        cookies = Cookies('testCookie=testValue; testCookie2=testValue2')
        with self.assertRaises(ValueError):
            cookies.removeCookie('testCookie3')

    def test_cookiePath(self):
        res = HTTPResponse(request, 'test')
        res.setCookie('test1', 'value')
        cookie = res.cookiesToSet['test1']
        self.assertEqual(cookie.path, '/page1/10/index')

    def test_cookieAttr(self):
        res = HTTPResponse(request, 'test')
        res.setCookie('test1', 'value', HTTPOnly=True)
        cookie = res.cookiesToSet['test1']
        self.assertEqual(str(cookie), 'test1=value; path=/page1/10/index; HttpOnly; ')
