from re import A
import unittest
from datetime import datetime
from pytz import timezone
from waffleweb.app import WaffleApp

from waffleweb.response import HTTPResponse
from waffleweb.wsgi import getResponseHeaders, getResponseStatus

class WsgiHandlerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.testResponse = HTTPResponse(content='Test Content')
        self.testResponse.setCookie('testCookie', 'testValue')

    def test_getResponseHeaders(self):
        headers = getResponseHeaders(self.testResponse)
        now = datetime.now(timezone('GMT'))
        dateTime = now.strftime("%a, %d %b %Y %X %Z")
        self.assertEqual(headers, [('Content-Type', 'text/html; charset=utf-8'),
                                    ('Date', f'{dateTime}'),
                                    ('Content-Length', '12'),
                                    ('Set-Cookie', 'testCookie=testValue; path=/; SameSite=Lax')])

    def test_getResponseStatus(self):
        self.assertEqual(getResponseStatus(self.testResponse), '200 OK')
