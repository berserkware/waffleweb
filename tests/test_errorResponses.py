from waffleweb.errorResponses import badRequest, notImplementedError, getErrorHandlerResponse
from waffleweb import WaffleApp
from waffleweb.request import Request
import unittest

from waffleweb.response import HTTPResponse

class BadRequestTest(unittest.TestCase):
    def test_debug(self):
        app = WaffleApp()

        self.assertEqual(badRequest(app, True).statusCode, 400)

    def test_noDebugNoHandler(self):
        app = WaffleApp()

        self.assertEqual(badRequest(app, False).content, b'400 Bad Request')

    def test_noDebugHandler(self):
        app = WaffleApp()

        @app.errorHandler(400)
        def badRequest():
            return HTTPResponse(content="handler content")

        self.assertEqual(badRequest().content, b'handler content')

class NotImplementedErrorTest(unittest.TestCase):
    def test_debugNoneResponse(self):
        app = WaffleApp()

        self.assertEqual(notImplementedError(None, True, 'GET').statusCode, 501)

    def test_debugResponse(self):
        app = WaffleApp()

        res = HTTPResponse(content='content') 
        self.assertEqual(notImplementedError(res, True, "GET").content, b'content')

    def test_noDebugNoneResponse(self):
        self.assertEqual(notImplementedError(None, False, "GET").content, b'Not Implemented Error')

    def test_noDebugResponse(self):
        res = HTTPResponse(content='response')
        self.assertEqual(notImplementedError(res, False, 'GET').content, b'response')

class GetErrorHandlerResponseTest(unittest.TestCase):
    def test_404Custom(self):       
        app = WaffleApp()
        
        @app.errorHandler(404)
        def handler(request):
            return HTTPResponse(request, '404 Page Handler')
            
        response = app.request(b'GET /testing404Page HTTP/1.1\r\n\r\n')

        self.assertEqual(response.content, b'404 Page Handler')
        
    def test_customErrorCode(self):
        app = WaffleApp()
        
        @app.errorHandler(220)
        def handler(request):
            return HTTPResponse(request, '220 Page')
            
        @app.route('/randomStatus')
        def randomStatus(request):
            return HTTPResponse(request, 'Random Status', status=220)
            
        response = app.request(b'GET /randomStatus HTTP/1.1\r\n\r\n')

        self.assertEqual(response.content, b'220 Page')
        
    def test_noErrorCodeHandler(self):

        app = WaffleApp()
        
        @app.route('/statusNoHandler')
        def statusNoHandler(request):
            return HTTPResponse(request, 'data')
            
        response = app.request(b'GET /statusNoHandler HTTP/1.1\r\n\r\n')

        self.assertEqual(response.content, b'data')
        
    def test_getErrorHandlerResponseByResponse(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        res = getErrorHandlerResponse(request=request, response=HTTPResponse(request, 'test', status=220))
        
        self.assertEqual(res.content, b'220 Page')
        
    def test_getErrorHandlerResponseByStatus(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        res = getErrorHandlerResponse(request=request, statusCode=220)
        
        self.assertEqual(res.content, b'220 Page')
        
    def test_getErrorHandlerResponseStatusNoHandler(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        res = getErrorHandlerResponse(request=request, statusCode=223)
        
        self.assertEqual(res, None)
        
    def test_getErrorHandlerResponseByResponseNoHandler(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )
        res = HTTPResponse(request, 'test', status=223)
        errorHandler = getErrorHandlerResponse(request=request, response=res)
        
        self.assertEqual(errorHandler.content, res.content)
