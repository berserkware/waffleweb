import unittest

from waffleweb.app import WaffleApp
from waffleweb.response import HTTPResponse
from waffleweb.exceptions import MiddlewareImportError, MiddlewareNotFoundError
from waffleweb.middleware import Middleware

class AppMiddlewareTest(unittest.TestCase):
    def test_beforeResponse(self):
        app = WaffleApp()
        
        app.middleware.append('middleware.appMiddletest.AppMiddletest')
        
        @app.route('/testBefore', methods=['GET', 'POST'])
        def testBefore(request):
            return HTTPResponse(request, request.POST)
            
        res = app.request(b'POST /testBefore HTTP/1.1\r\nContent-Length: 25\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\ntest1=test2')
        self.assertEqual(res.content, b'{}')

    def test_afterResponse(self):
        app = WaffleApp()
        
        app.middleware.append('middleware.appMiddletest.AppMiddletest')
        
        @app.route('/')
        def testAfter(request):
            return HTTPResponse(request, 'not middlewared')
            
        res = app.request(b'GET / HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'middlewareified')
        
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