import unittest
from waffleweb import middleware

from waffleweb.app import WaffleApp
from waffleweb.request import Request
from waffleweb.response import HTTPResponse
from waffleweb.exceptions import MiddlewareImportError, MiddlewareNotFoundError
from waffleweb.middleware import runRequestMiddleware, runResponseMiddleware

from middleware.appMiddletest import AppMiddletest
from middleware.noFunctionsMiddleware import NoFunctions

class RunMiddlewareTest(unittest.TestCase):
    def test_beforeResponse(self):
        request = Request(b'GET / HTTP/1.1\r\nTest-Header: value\r\n\r\n', '172.0.0.1')

        request = runRequestMiddleware(request, [AppMiddletest])

        self.assertEqual(request.META['TEST_HEADER'], 'value2')

    def test_afterResponse(self):
        res = HTTPResponse(content='test')

        res = runResponseMiddleware(res, [AppMiddletest])

        self.assertEqual(res.content, b'middlewareified')
 
    def test_beforeRequestNoMethod(self):
        request = Request(b'GET / HTTP/1.1\r\nTest-Header: value\r\n\r\n', '172.0.0.1')

        request = runRequestMiddleware(request, [NoFunctions])

        self.assertEqual(request.META['TEST_HEADER'], 'value')

    def test_afterResponseNoMethod(self):
        response = HTTPResponse(content='test')
        response = runResponseMiddleware(response, [NoFunctions])

        self.assertEqual(response.content, b'test')

    def test_beforeRequestNoMiddleware(self):
        request = Request(b'GET / HTTP/1.1\r\nTest-Header: value\r\n\r\n', '172.0.0.1')

        request = runRequestMiddleware(request, [])

        self.assertEqual(request.META['TEST_HEADER'], 'value')

    def test_afterResponseNoMiddleware(self):
        response = HTTPResponse(content='test')
        response = runResponseMiddleware(response, [])

        self.assertEqual(response.content, b'test')