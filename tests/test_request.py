from waffleweb.app import WaffleApp
from waffleweb.request import Request, findView, matchVariableInURL

import unittest
import waffleweb

from waffleweb.response import HTTP404, HTTPResponse
from waffleweb.datatypes import MultiValueOneKeyDict

class RequestTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RequestTest, self).__init__(*args, **kwargs)
        self.request = Request(b'GET /math/ HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nCookie: addedCookie=32\r\nHost: localhost:8080\r\n\r\ntestData1=321&testData2=123', IP='127.0.0.1')

    def test_path(self):
        self.assertEqual(self.request.path, '/math/')

    def test_method(self):
        self.assertEqual(self.request.method, 'GET')

    def test_HTTPVersion(self):
        self.assertEqual(self.request.HTTPVersion, 'HTTP/1.1')

    def test_META(self):
        self.assertEqual(self.request.META,
            MultiValueOneKeyDict({
                'USER_AGENT': 'PostmanRuntime/7.29.0',
                'ACCEPT': '*/*',
                'ACCEPT_ENCODING': 'gzip, deflate, br',
                'CONNECTION': 'keep-alive',
                'COOKIE': 'addedCookie=32',
                'HOST': 'localhost:8080'
            })
        )

    def test_IP(self):
        self.assertEqual(self.request.IP, '127.0.0.1')

    def test_body(self):
        self.assertEqual(self.request.body, b'\ntestData1=321&testData2=123')

    def test_FILES(self):
        req = Request(b'POST /filesPostTest/ HTTP/1.1\r\nContent-Length: 173\r\nContent-Type: multipart/form-data; boundary=6b31468dd2655947891a2a312ab9346b\r\n\r\n--6b31468dd2655947891a2a312ab9346b\r\nContent-Disposition: form-data; name="test"; filename="test.html"\r\n\r\n<h1>Testing Testing 123</h1>\r\n--6b31468dd2655947891a2a312ab9346b--\r\n', '127.0.0.1')
        self.assertEqual(b'<h1>Testing Testing 123</h1>', req.FILES['test'].data)
        
class MatchVariableInURLTest(unittest.TestCase):
    def test_convertToIntCorrect(self):
        indexOfVar = 1
        urlVarData = ['test', 'int']
        splitUri = ['test', '5']
        
        matched = matchVariableInURL(indexOfVar, urlVarData, splitUri)
        
        self.assertEqual(matched[1], 5)
        
    def test_convertToIntNotAInt(self):
        indexOfVar = 1
        urlVarData = ['test', 'int']
        splitUri = ['test', 'not']
        
        matched = matchVariableInURL(indexOfVar, urlVarData, splitUri)
        
        self.assertEqual(matched[1], 'not')
        
    def test_convertToFloatCorrect(self):
        indexOfVar = 1
        urlVarData = ['test', 'float']
        splitUri = ['test', '5.5']
        
        matched = matchVariableInURL(indexOfVar, urlVarData, splitUri)
        
        self.assertEqual(matched[1], 5.5)
        
    def test_convertToFloatNotAFloat(self):
        indexOfVar = 1
        urlVarData = ['test', 'float']
        splitUri = ['test', 'not']
        
        matched = matchVariableInURL(indexOfVar, urlVarData, splitUri)
        
        self.assertEqual(matched[1], 'not')
        
    def test_convertToStrCorrect(self):
        indexOfVar = 1
        urlVarData = ['test', 'str']
        splitUri = ['test', 'hello']
        
        matched = matchVariableInURL(indexOfVar, urlVarData, splitUri)
        
        self.assertEqual(matched[1], 'hello')
        
class FindViewTest(unittest.TestCase):
    def test_exactURLMatch(self):
        app = WaffleApp()
        
        @app.route('/test')
        def test(request):
            return HTTPResponse(request, 'test')
            
        waffleweb.currentWorkingApp = app
            
        req = Request(b'GET /test HTTP/1.1', '127.0.0.1')
        view = findView(req)
        
        self.assertEqual(view[0].view(None).content, test(None).content)
        
    def test_URLWrong(self):
        app = WaffleApp()
        
        @app.route('/test')
        def test(request):
            return HTTPResponse(request, 'test')
            
        waffleweb.currentWorkingApp = app
            
        req = Request(b'GET /wrong HTTP/1.1', '127.0.0.1')
        with self.assertRaises(HTTP404):
            view = findView(req)
            
    def test_MultipleSectorURLMatch(self):
        app = WaffleApp()
        
        @app.route('/test/more')
        def test(request):
            return HTTPResponse(request, 'test')
            
        waffleweb.currentWorkingApp = app
            
        req = Request(b'GET /test/more HTTP/1.1', '127.0.0.1')
        view = findView(req)
        
        self.assertEqual(view[0].view(None).content, test(None).content)
        
    def test_MultipleSectorURLWrong(self):
        app = WaffleApp()
        
        @app.route('/test/more')
        def test(request):
            return HTTPResponse(request, 'test')
            
        waffleweb.currentWorkingApp = app
            
        req = Request(b'GET /test HTTP/1.1', '127.0.0.1')
        with self.assertRaises(HTTP404):
            view = findView(req)
            
    def test_MultipleSectorAndOneSectorURLCorrect(self):
        app = WaffleApp()
        
        @app.route('/test/more')
        def test(request):
            return HTTPResponse(request, 'test')
            
        @app.route('/test')
        def test2(request):
            return HTTPResponse(request, 'test2')
            
        waffleweb.currentWorkingApp = app
            
        req = Request(b'GET /test/more HTTP/1.1', '127.0.0.1')
        view = findView(req)
        
        self.assertEqual(view[0].view(None).content, test(None).content)
        
        req = Request(b'GET /test HTTP/1.1', '127.0.0.1')
        view = findView(req)
        
        self.assertEqual(view[0].view(None).content, test2(None).content)
        
    def test_URLVariablesURLCorrect(self):
        app = WaffleApp()
        
        @app.route('/test/<test:int>')
        def test(request):
            return HTTPResponse(request, 'test')
            
        waffleweb.currentWorkingApp = app
            
        req = Request(b'GET /test/5 HTTP/1.1', '127.0.0.1')
        view = findView(req)
        
        self.assertEqual(view[0].view(None).content, test(None).content)
        
    def test_URLVariablesURLIncorrect(self):
        app = WaffleApp()
        
        @app.route('/test/<test:int>')
        def test(request):
            return HTTPResponse(request, 'test')
            
        waffleweb.currentWorkingApp = app
            
        req = Request(b'GET /test HTTP/1.1', '127.0.0.1')
        with self.assertRaises(HTTP404):
            view = findView(req)