import unittest
import waffleweb

from waffleweb import WaffleApp
from waffleweb.errorResponses import MethodNotAllowed
from waffleweb.response import HTTPResponse, JSONResponse, FileResponse
from waffleweb.request import Request, findView
from waffleweb.methodHandler import handleHead, handleOptions, handleOther

class HandleGetTest(unittest.TestCase):
    def test_getAndHeadNotInAllowedMethodsNoErrorHandler(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['POST'])
        def test(request):
            return HTTPResponse(request, 'test')
            
        view = app.views[-1]
        
        response = handleHead(view, {}, None, False)
        
        self.assertEqual(type(response), MethodNotAllowed)
        
    def test_getAndHeadNotInAllowedMethodsErrorHandlerPresent(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['POST'])
        def test(request):
            return HTTPResponse(request, 'test')
            
        @app.errorHandler(405)
        def methodNotAllowed(request):
            return HTTPResponse(request, 'handled', status=405)
            
        view = app.views[-1]
        
        waffleweb.currentWorkingApp = app
        
        response = handleHead(view, {}, None, False)
        
        self.assertEqual(response.content, b'handled')
        
        waffleweb.currentWorkingApp = waffleweb.app
        
        
    def test_removeContentHTTPResponse(self):
        
        app = WaffleApp()
        
        @app.route('/test', methods=['GET'])
        def test(request):
            return HTTPResponse(request, 'test')
            
        view = app.views[-1]
        
        response = handleHead(view, {}, None, False)
        
        self.assertEqual(response.content, b'')
        
    def test_removeContentJSONResponse(self):
        
        app = WaffleApp()
        
        @app.route('/test', methods=['GET'])
        def test(request):
            return JSONResponse(request, {'test': 'test'})
            
        view = app.views[-1]
        
        response = handleHead(view, {}, None, False)
        
        self.assertEqual(response.content, b'')
        
    def test_removeContentFileResponse(self):
        
        app = WaffleApp()
        
        @app.route('/test', methods=['GET'])
        def test(request):
            with open('testtext.txt', 'r') as f:
                return FileResponse(request, f)
            
        view = app.views[-1]
        
        response = handleHead(view, {}, None, False)
        
        self.assertEqual(response.content, b'')
        
class HandleOptionsTest(unittest.TestCase):
    def test_getAndHeadNotInAllowedMethodsNoErrorHandler(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['POST'])
        def test(request):
            return HTTPResponse(request, 'test')
            
        view = app.views[-1]
        
        response = handleOptions(view, None, False)
        
        self.assertEqual(type(response), MethodNotAllowed)
        
    def test_getAndHeadNotInAllowedMethodsErrorHandlerPresent(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['POST'])
        def test(request):
            return HTTPResponse(request, 'test')
            
        @app.errorHandler(405)
        def methodNotAllowed(request):
            return HTTPResponse(request, 'handled', status=405)
            
        view = app.views[-1]
        
        waffleweb.currentWorkingApp = app
        
        response = handleOptions(view, None, False)
        
        self.assertEqual(response.content, b'handled')
        
        waffleweb.currentWorkingApp = waffleweb.app
        
    def test_onlyGet(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['GET'])
        def test(request):
            return HTTPResponse(request, 'test')
        
        view = app.views[-1]
        
        response = handleOptions(view, None, False)
        
        self.assertEqual(response.headers['Allow'], 'GET, HEAD, OPTIONS')
        
    def test_noGet(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['POST'])
        def test(request):
            return HTTPResponse(request, 'test')
        
        view = app.views[-1]
        
        response = handleOptions(view, None, False)
        
        self.assertEqual(response.headers['Allow'], 'POST')
        
    def test_getAndOtherMethods(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['POST', 'GET'])
        def test(request):
            return HTTPResponse(request, 'test')
        
        view = app.views[-1]
        
        response = handleOptions(view, None, False)
        
        self.assertEqual(response.headers['Allow'], 'POST, GET, HEAD, OPTIONS')
        
class HandleOtherTest(unittest.TestCase):
    def test_getAndHeadNotInAllowedMethodsNoErrorHandler(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['POST'])
        def test(request):
            return HTTPResponse(request, 'test')
            
        view = app.views[-1]
        
        req = Request(b'GET / HTTP/1.1', '127.0.0.1')
        
        response = handleOther(view, {}, req, False)
        
        self.assertEqual(type(response), MethodNotAllowed)
        
    def test_getAndHeadNotInAllowedMethodsErrorHandlerPresent(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['POST'])
        def test(request):
            return HTTPResponse(request, 'test')
            
        @app.errorHandler(405)
        def methodNotAllowed(request):
            return HTTPResponse(request, 'handled', status=405)
            
        view = app.views[-1]
        
        waffleweb.currentWorkingApp = app
        
        req = Request(b'GET / HTTP/1.1', '127.0.0.1')
        
        response = handleOther(view, {}, req, False)
        
        self.assertEqual(response.content, b'handled')
        
        waffleweb.currentWorkingApp = waffleweb.app
        
        
    def test_getAndOtherMethods(self):
        app = WaffleApp()
        
        @app.route('/test', methods=['GET'])
        def test(request):
            return HTTPResponse(request, 'test')
        
        view = app.views[-1]
        
        req = Request(b'GET / HTTP/1.1', '127.0.0.1')
        
        response = handleOther(view, {}, req, False)
        
        self.assertEqual(response.content, b'test')