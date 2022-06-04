from re import A
import unittest
from datetime import datetime
from pytz import timezone

from waffleweb.middleware import MiddlewareHandler
from waffleweb.response import HTTPResponse
from waffleweb.wsgi import WsgiHandler

class WsgiHandlerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open('tests/static/test.html', 'rb') as f:
            testEnviron = {'wsgi.input': f, 'SERVER_SOFTWARE': 'gunicorn/20.1.0', 'REQUEST_METHOD': 'GET',
            'QUERY_STRING': '', 'RAW_URI': '/', 'SERVER_PROTOCOL': 'HTTP/1.1', 'HTTP_HOST': 'localhost:8000', 
            'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0', 'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'HTTP_ACCEPT_LANGUAGE': 'en-US,en;q=0.5', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br', 
            'HTTP_CONNECTION': 'keep-alive', 'HTTP_UPGRADE_INSECURE_REQUESTS': '1', 'HTTP_SEC_FETCH_DEST': 'document',
            'HTTP_SEC_FETCH_MODE': 'navigate', 'HTTP_SEC_FETCH_SITE': 'none', 
            'HTTP_SEC_FETCH_USER': '?1', 'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': '47636', 'SERVER_NAME': '127.0.0.1', 
            'SERVER_PORT': '8000', 'PATH_INFO': '/', 'SCRIPT_NAME': ''}        
            self.wsgiHandler = WsgiHandler(testEnviron, apps=[], middlewareHandler=MiddlewareHandler([]))
            testResponse = HTTPResponse(content='Test Content')
            testResponse.setCookie('testCookie', 'testValue')
            self.wsgiHandler.response = testResponse

    def test_getResponseContent(self):
        self.assertEqual(self.wsgiHandler.getResponseContent(), b'Test Content')

    def test_getResponseHeaders(self):
        headers = self.wsgiHandler.getResponseHeaders()
        now = datetime.now(timezone('GMT'))
        dateTime = now.strftime("%a, %d %b %Y %X %Z")
        self.assertEqual(headers, [('Content-Type', 'text/html; charset=utf-8'),
                                    ('Date', f'{dateTime}'),
                                    ('Content-Length', '12'),
                                    ('Set-Cookie', 'testCookie=testValue; path=/; SameSite=Lax')])

    def test_getResponseStatus(self):
        self.assertEqual(self.wsgiHandler.getResponseStatus(), '200 OK')