import json
import unittest
import requests
from datetime import datetime
from pytz import timezone

from waffleweb.request import Request, RequestHandler
from waffleweb.response import HTTPResponse, JSONResponse
from waffleweb import WaffleApp

class SplitUrlTest(unittest.TestCase):
    def test_splitURLNormal(self):
        request = Request(
            b'GET /page1/10/index HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request)

        self.assertEqual(handler._splitURL(), ('/page1/10/index', ['page1', '10', 'index'], ''))

    def test_splitUrlWithExt(self):
        request = Request(
            b'GET /test/testExt.jpg HTTP/1.1\r\n\r\n', 
            '127.0.0.1'
            )

        handler = RequestHandler(request)

        self.assertEqual(handler._splitURL(), ('/test/testExt', ['test', 'testExt'], '.jpg'))

    def test_splitUrlNone(self):
        request = Request(
            b'GET / HTTP/1.1\r\n\r\n',
            '127.0.0.1'
            )
            
        handler = RequestHandler(request)

        self.assertEqual(handler._splitURL(), ('/', [''], ''))

class HandleTest(unittest.TestCase):
    def test_handleGet(self):
        app = WaffleApp()
        
        @app.route('math/<operator:str>/<num1:int>/<num2:int>', 'basicMath', ['GET', 'POST'])
        def basicMath(request, operator, num1, num2):
            if operator == 'add':
                result = {'answer': num1 + num2}
            elif operator == 'subtract':
                result = {'answer': num1 - num2}
            elif operator == 'multiply':
                result = {'answer': num1 * num2}
            elif operator == 'divide':
                result = {'answer': num1 / num2}
            else:
                result = {'error': 'Unknown operator'}

            return JSONResponse(request, result)
            
        response = app.request(b'GET /math/add/1/1 HTTP/1.1\r\n\r\n')
        
        self.assertEqual(response.statusCode, 200)
        self.assertEqual(json.loads(response.content.decode()), {'answer': 2})

class GetTest(unittest.TestCase):
    def test_statusCode(self):
        app = WaffleApp()
        
        @app.route('/index')
        def index(request):
            return HTTPResponse(request, 'index')
            
        response = app.request(b'GET /index HTTP/1.1\r\n\r\n')
        self.assertEqual(response.statusCode, 200)

    def test_correctContent(self):
        app = WaffleApp()
        
        @app.route('math/<operator:str>/<num1:int>/<num2:int>', 'basicMath', ['GET', 'POST'])
        def basicMath(request, operator, num1, num2):
            if operator == 'add':
                result = {'answer': num1 + num2}
            elif operator == 'subtract':
                result = {'answer': num1 - num2}
            elif operator == 'multiply':
                result = {'answer': num1 * num2}
            elif operator == 'divide':
                result = {'answer': num1 / num2}
            else:
                result = {'error': 'Unknown operator'}

            return JSONResponse(request, result)
            
        response = app.request(b'GET /math/add/1/1 HTTP/1.1\r\n\r\n')
        self.assertEqual(json.loads(response.content.decode()), {'answer': 2})

class HeadTest(unittest.TestCase):
    def test_allHeadersCorrect(self):
        app = WaffleApp()
        
        @app.route('/index')
        def index(request):
            return HTTPResponse(request, 'index')
            
        response = app.request(b'HEAD /index HTTP/1.1\r\n\r\n')
        
        now = datetime.now(timezone('GMT'))
        dateTime = now.strftime("%a, %d %b %Y %X %Z")

        self.assertEqual(response.headers._data, {
            'Content-Type': ['text/html; charset=utf-8'],
            'Date': [dateTime],
            'Content-Length': ['0']
            })

    def test_noContent(self):
        app = WaffleApp()
        
        @app.route('/index')
        def index(request):
            return HTTPResponse(request, 'index')
            
        response = app.request(b'HEAD /index HTTP/1.1\r\n\r\n')
        
        self.assertEqual(response.content, b'')

class PostTest(unittest.TestCase):
    def test_correctData(self):
        req = Request(b'POST /math/postTest/ HTTP/1.1\r\nContent-Length: 25\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\ntestData1=15&testData2=30', '127.0.0.1')
        self.assertEqual(req.POST, {'testData1': '15', 'testData2': '30'})

class OptionsTest(unittest.TestCase):
    def test_correctHeaders(self):
        app = WaffleApp()
        
        @app.route('/index')
        def index(request):
            return HTTPResponse(request, 'index')
            
        response = app.request(b'OPTIONS /index HTTP/1.1\r\n\r\n')
        
        now = datetime.now(timezone('GMT'))
        dateTime = now.strftime("%a, %d %b %Y %X %Z")

        self.assertEqual(response.headers._data, {
            'Allow': ['GET, HEAD, OPTIONS'],
            'Content-Type': ['text/html; charset=utf-8'],
            'Date': [dateTime],
            'Content-Length': ['0'],
            })

class MethodTest(unittest.TestCase):
    def test_methodNotAllowed(self):
        app = WaffleApp()
        
        @app.route('/', 'index', ['GET'])
        def index(request):
            return HTTPResponse(request, 'data')
            
        response = app.request(b'POST / HTTP/1.1\r\n\r\n')
        self.assertEqual(response.statusCode, 405)

    def test_methodAllowed(self):
        app = WaffleApp()
        
        @app.route('/', 'index', ['GET'])
        def index(request):
            return HTTPResponse(request, 'data')
            
        response = app.request(b'GET / HTTP/1.1\r\n\r\n')
        self.assertEqual(response.statusCode, 200)
        
class ErrorHandlerTest(unittest.TestCase):
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

        handler = RequestHandler(request)
        res = handler.getErrorHandlerResponse(response=HTTPResponse(request, 'test', status=220))
        
        self.assertEqual(res.content, b'220 Page')
        
    def test_getErrorHandlerResponseByStatus(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request)
        res = handler.getErrorHandlerResponse(statusCode=220)
        
        self.assertEqual(res.content, b'220 Page')
        
    def test_getErrorHandlerResponseStatusNoHandler(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request)
        res = handler.getErrorHandlerResponse(statusCode=223)
        
        self.assertEqual(res, None)
        
    def test_getErrorHandlerResponseByResponseNoHandler(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )
        res = HTTPResponse(request, 'test', status=223)
        handler = RequestHandler(request)
        errorHandler = handler.getErrorHandlerResponse(response=res)
        
        self.assertEqual(errorHandler.content, res.content)
