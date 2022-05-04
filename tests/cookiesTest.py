import unittest

import requests
from waffleweb import WaffleApp
from waffleweb.request import Request
from waffleweb.response import HTTPResponse
from waffleweb.cookie import Cookies

class basicCookieTest(unittest.TestCase):
    def test_cookie(self):
        with requests.Session() as s:
            request = s.get('http://localhost:8080/cookieTest')
            self.assertEqual(s.cookies.get_dict(), {'testCookie': 'testVal'})

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


