import unittest

from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse

class BasicRouteTest(unittest.TestCase):
    def test_pathInvalidRelitiveURL(self):
        app = WaffleApp()

        with self.assertRaises(ValueError):
            @app.route('www.google.com', 'index')
            def index(request=None):
                pass    

            index()
    
    def test_pathValidRelitiveURL(self):
        app = WaffleApp()
        
        try:
            @app.route('/home/index', 'index')
            def index(request=None):
                pass    

            index()
        except ValueError:
            self.fail('index() raised ValueError unexpectably')

    def test_argumentsFail(self):
        app = WaffleApp()

        with self.assertRaises(AttributeError):
            @app.route('/index/arg1:str>/<int:arg2>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

            index(request=None)

    def test_argumentsRaiseAttributeError(self):
        app = WaffleApp()
        with self.assertRaises(AttributeError):
            @app.route('/index/<arg1:int>/<arg2:notAValidType>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

            index(request=None)

    def test_argumentsRaiseAttributeError2(self):
        app = WaffleApp()
        
        with self.assertRaises(AttributeError):
            @app.route('/index/<arg1>/<arg2>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

            index(request=None)
    
    def test_arguments(self):
        app = WaffleApp()
        
        @app.route('/article/<name:str>')
        def article(request, name):
            return HTTPResponse(request, f"{name}")
            
        res = app.request(b'GET /article/test HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'test')
        
class ErrorHandlerTest(unittest.TestCase):
    def test_statusTooBig(self):
        with self.assertRaises(ValueError):
            app = WaffleApp()
            
            @app.errorHandler(700)
            def handler(request):
                return HTTPResponse(request, '700')
            
    def test_statusTooSmall(self):
        with self.assertRaises(ValueError):
            app = WaffleApp()
            
            @app.errorHandler(50)
            def handler(request):
                return HTTPResponse(request, '50')
                
    def test_statusJustRight(self):
        try:
            app = WaffleApp()
            
            @app.errorHandler(404)
            def handler(request):
                return HTTPResponse(request, '404')
        except ValueError:
            self.fail('A ValueError was raised.')
        
class requestTest(unittest.TestCase):
    def test_basic(self):
        app = WaffleApp()
        
        @app.route('/index')
        def index(request):
            return HTTPResponse(request, 'index')
            
        res = app.request(b'GET /index HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'index')
        
    def test_withArgs(self):
        app = WaffleApp()
        
        @app.route('/article/<name:str>')
        def article(request, name):
            return HTTPResponse(request, name)
            
        res = app.request(b'GET /article/test HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'test')
        
    def test_withMiddleware(self):
        app = WaffleApp()
        
        app.middleware.append('middleware.testMiddleware.TestMiddleware')
        
        @app.route('/page')
        def page(request):
            return HTTPResponse(request, f'{request.META["middlewareHeader2"]}')
            
        res = app.request(b'GET /page HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'value')
        self.assertEqual(res.headers['middlewareHeader'], 'value')
        
    def test_404(self):
        app = WaffleApp()
        
        @app.route('/page')
        def page(request):
            return HTTPResponse(request, 'page')
            
        res = app.request(b'GET /existnt HTTP/1.1\r\n\r\n')
        self.assertEqual(res.statusCode, 404)
        
    def test_errorHandler(self):
        app = WaffleApp()
        
        @app.errorHandler(404)
        def handler(request):
            return HTTPResponse(request, '404')
            
        res = app.request(b'GET /existnt HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'404')