import unittest
from waffleweb import middleware

from waffleweb.app import WaffleApp
from waffleweb.request import Request
from waffleweb.response import HTTPResponse
from waffleweb.exceptions import MiddlewareImportError, MiddlewareNotFoundError
from waffleweb.middleware import Middleware, runRequestMiddleware, runResponseMiddleware

class RunMiddlewareTest(unittest.TestCase):
    def test_beforeResponse(self):
        middleware = Middleware()
        
        middleware.append('middleware.appMiddletest.AppMiddletest')

        request = Request(b'GET / HTTP/1.1\r\nTest-Header: value\r\n\r\n', '172.0.0.1')

        request = runRequestMiddleware(request, middleware)

        self.assertEqual(request.META['TEST_HEADER'], 'value2')

    def test_afterResponse(self):
        middleware = Middleware()

        middleware.append('middleware.appMiddletest.AppMiddletest')

        res = HTTPResponse(content='test')

        res = runResponseMiddleware(res, middleware)

        self.assertEqual(res.content, b'middlewareified')
 
    def test_beforeRequestNoMethod(self):
        middleware = Middleware(['middleware.noFunctionsMiddleware.NoFunctions'])
        
        request = Request(b'GET / HTTP/1.1\r\nTest-Header: value\r\n\r\n', '172.0.0.1')

        request = runRequestMiddleware(request, middleware)

        self.assertEqual(request.META['TEST_HEADER'], 'value')

    def test_afterResponseNoMethod(self):
        middleware = Middleware(['middleware.noFunctionsMiddleware.NoFunctions'])
        response = HTTPResponse(content='test')
        response = runResponseMiddleware(response, middleware)

        self.assertEqual(response.content, b'test')

    def test_beforeRequestNoMiddleware(self):
        middleware = Middleware()
        
        request = Request(b'GET / HTTP/1.1\r\nTest-Header: value\r\n\r\n', '172.0.0.1')

        request = runRequestMiddleware(request, middleware)

        self.assertEqual(request.META['TEST_HEADER'], 'value')

    def test_afterResponseNoMiddleware(self):
        middleware = Middleware()
        response = HTTPResponse(content='test')
        response = runResponseMiddleware(response, middleware)

        self.assertEqual(response.content, b'test')


class AddMiddlewareTest(unittest.TestCase):
    def test_appendMiddleware(self):
        middleware = Middleware()
        
        try:
            middleware.append('middleware.appMiddletest.AppMiddletest')
        except (MiddlewareImportError, MiddlewareNotFoundError):
            self.fail('Error importing middleware.')
            
    def test_appendMiddlewareNotFoundError(self):
        middleware = Middleware()
        
        with self.assertRaises(MiddlewareNotFoundError):
            middleware.append('file.DoesntExist')
            
    def test_appendMiddlewareImportError(self):
        middleware = Middleware()
        
        with self.assertRaises(MiddlewareImportError):
            middleware.append('file')
            
    def test_overwriteMiddleware(self):
        middleware = Middleware()
        
        try:
            middleware.append('middleware.appMiddletest.AppMiddletest')
            middleware[0] = 'middleware.testMiddleware.TestMiddleware'
        except (MiddlewareImportError, MiddlewareNotFoundError):
            self.fail('Error importing middleware.')
            
    def test_overwriteMiddlewareNotFoundError(self):
        middleware = Middleware()
        
        with self.assertRaises(MiddlewareNotFoundError):
            middleware.append('middleware.appMiddletest.AppMiddletest')
            middleware[0] = 'file.NotExist'
            
    def test_overwriteMiddlewareImportError(self):
        middleware = Middleware()
        
        with self.assertRaises(MiddlewareImportError):
            middleware.append('middleware.appMiddletest.AppMiddletest')
            middleware[0] = 'file'
            
    def test_overwriteMiddlewareIndexError(self):
        middleware = Middleware()
        
        with self.assertRaises(IndexError):
            middleware.append('middleware.appMiddletest.AppMiddletest')
            middleware[1] = 'middleware.testMiddleware.TestMiddleware'
