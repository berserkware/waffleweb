import unittest

from waffleweb.app import WaffleApp
from waffleweb.response import HTTPResponse

class AppMiddlewareTest(unittest.TestCase):
    def test_beforeResponse(self):
        app = WaffleApp('testApp', middleware=['middleware.appMiddletest.AppMiddletest'])
        
        @app.route('/testBefore', methods=['GET', 'POST'])
        def testBefore(request):
            return HTTPResponse(request, request.POST)
            
        res = app.request(b'POST /testBefore HTTP/1.1\r\nContent-Length: 25\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\ntest1=test2')
        self.assertEqual(res.content, b'{}')

    def test_afterResponse(self):
        app = WaffleApp('testApp', middleware=['middleware.appMiddletest.AppMiddletest'])
        
        @app.route('/')
        def testAfter(request):
            return HTTPResponse(request, 'not middlewared')
            
        res = app.request(b'GET / HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'middlewareified')