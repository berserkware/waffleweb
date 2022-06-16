import unittest
import requests
from datetime import datetime
from pytz import timezone

from waffleweb.request import Request, RequestHandler
from waffleweb.response import HTTPResponse

class ParamsTest(unittest.TestCase):
    def test_paramsNormal(self):
        res = requests.get('http://localhost:8080/paramTest/?test=134&test2=31').json()
        self.assertEqual(res, {'test':'134', 'test2':'31'})

    def test_paramsRedirect(self):
        res = requests.get('http://localhost:8080/paramTest?test=134&test2=31').json()
        self.assertEqual(res, {'test':'134', 'test2':'31'})

    def test_paramsNone(self):
        res = requests.get('http://localhost:8080/paramTest/?').json()
        self.assertEqual(res, {})

    def test_paramsOneParam(self):
        res = requests.get('http://localhost:8080/paramTest?test=134').json()
        self.assertEqual(res, {'test':'134'})

    def test_paramsWithMultipleQuestionMarks(self):
        res = requests.get('http://localhost:8080/paramTest?te?st=134&test2=3?1').json()
        self.assertEqual(res, {'te?st':'134', 'test2':'3?1'})


class SplitUrlTest(unittest.TestCase):
    def test_splitURLNormal(self):
        request = Request(
            'GET /page1/10/index HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request, [])

        self.assertEqual(handler._splitURL(), ('/page1/10/index', ['page1', '10', 'index'], ''))

    def test_splitUrlWithExt(self):
        request = Request(
            'GET /test/testExt.jpg HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\n\r\n', 
            '127.0.0.1'
            )

        handler = RequestHandler(request, [])

        self.assertEqual(handler._splitURL(), ('/test/testExt', ['test', 'testExt'], '.jpg'))

    def test_splitUrlNone(self):
        request = Request(
            'GET / HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n',
            '127.0.0.1'
            )

        handler = RequestHandler(request, [])

        self.assertEqual(handler._splitURL(), ('/', [''], ''))

class HandleTest(unittest.TestCase):
    def test_handleGet(self):
        response = requests.get('http://localhost:8080/math/add/1/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'answer': 2})

class GetTest(unittest.TestCase):
    def test_statusCode(self):
        response = requests.get('http://localhost:8080/math/add/1/1')
        self.assertEqual(response.status_code, 200)

    def test_correctContent(self):
        response = requests.get('http://localhost:8080/math/add/1/1')
        self.assertEqual(response.json(), {'answer': 2})

class HeadTest(unittest.TestCase):
    def test_allHeadersCorrect(self):
        response = requests.head('http://localhost:8080/math/')
        now = datetime.now(timezone('GMT'))
        dateTime = now.strftime("%a, %d %b %Y %X %Z")

        headers = response.headers
        try:
            del headers['Server']
            del headers['Connection']
        except:
            pass

        self.assertEqual(response.headers, {
            'Content-Type': 'text/html; charset=utf-8',
            'Date': dateTime,
            'Content-Length': '0',
            'Set-Cookie': 'addedCookie=32; path=/math/; SameSite=Lax',
            })

    def test_noContent(self):
        response = requests.head('http://localhost:8080/math/')
        self.assertEqual(response.content, b'')

class PostTest(unittest.TestCase):
    def test_correctData(self):
        data = {'testData1': 15, 'testData2': 30}
        response = requests.post('http://localhost:8080/math/postTest/', data=data)
        self.assertEqual(response.content, b"{'testData1': '15', 'testData2': '30'}")

class OptionsTest(unittest.TestCase):
    def test_correctHeaders(self):
        response = requests.options('http://localhost:8080/math/')
        now = datetime.now(timezone('GMT'))
        dateTime = now.strftime("%a, %d %b %Y %X %Z")

        headers = dict(response.headers)
        try:
            del headers['Server']
            del headers['Connection']
        except:
            pass

        self.assertEqual(headers, {
            'Allow': 'OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT',
            'Content-Type': 'text/html; charset=utf-8',
            'Date': dateTime,
            'Content-Length': '0',
            'Set-Cookie': 'addedCookie=32; path=/; SameSite=Lax',
            })

class MethodTest(unittest.TestCase):
    def test_methodNotAllowed(self):
        response = requests.get('http://localhost:8080/math/postTest/')
        self.assertEqual(response.status_code, 405)

    def test_methodAllowed(self):
        response = requests.get('http://localhost:8080/math/add/1/1')
        self.assertEqual(response.status_code, 200)
        
class ErrorHandlerTest(unittest.TestCase):
    def test_404Custom(self):
        request = Request(
            'GET /testing404Page HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request, [])
        
        response = handler.getResponse()
        self.assertEqual(response.content, b'404 Page Handler')
        
    def test_customErrorCode(self):
        request = Request(
            'GET /randomStatus HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request, [])
        
        response = handler.getResponse()
        self.assertEqual(response.content, b'220 Page')
        
    def test_noErrorCodeHandler(self):
        request = Request(
            'GET /statusNoHandler HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request, [])
        
        response = handler.getResponse()
        self.assertEqual(response.content, b'status but no handler.')
        
    def test_getErrorHandlerByResponse(self):
        request = Request(
            'GET /statusNoHandler HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request, [])
        res = handler.getErrorHandler(response=HTTPResponse(request, 'test', status=220))
        
        self.assertEqual(res.content, b'220 Page')
        
    def test_getErrorHandlerByStatus(self):
        request = Request(
            'GET /statusNoHandler HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request, [])
        res = handler.getErrorHandler(statusCode=220)
        
        self.assertEqual(res.content, b'220 Page')
        
    def test_getErrorHandlerStatusNoHandler(self):
        request = Request(
            'GET /statusNoHandler HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n', 
            '101.98.137.19'
            )

        handler = RequestHandler(request, [])
        res = handler.getErrorHandler(statusCode=223)
        
        self.assertEqual(res, None)
        
    def test_getErrorHandlerByResponseNoHandler(self):
        request = Request(
            'GET /statusNoHandler HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\n', 
            '101.98.137.19'
            )
        res = HTTPResponse(request, 'test', status=223)
        handler = RequestHandler(request, [])
        errorHandler = handler.getErrorHandler(response=res)
        
        self.assertEqual(errorHandler.content, res.content)