import unittest

from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse

class BasicRouteTest(unittest.TestCase):
    def test_pathInvalidRelitiveURL(self):
        app = WaffleApp('test')

        with self.assertRaises(ValueError):
            @app.route('www.google.com', 'index')
            def index(request=None):
                pass    

            index()
    
    def test_pathValidRelitiveURL(self):
        app = WaffleApp('test')
        try:
            @app.route('/home/index', 'index')
            def index(request=None):
                pass    

            index()
        except ValueError:
            self.fail('index() raised ValueError unexpectably')

    def test_argumentsFail(self):
        app = WaffleApp('test')

        with self.assertRaises(AttributeError):
            @app.route('/index/arg1:str>/<int:arg2>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

            index(request=None)

    def test_argumentsRaiseAttributeError(self):
        app = WaffleApp('test')
        with self.assertRaises(AttributeError):
            @app.route('/index/<arg1:int>/<arg2:notAValidType>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

            index(request=None)

    def test_argumentsRaiseAttributeError2(self):
        app = WaffleApp('test')
        with self.assertRaises(AttributeError):
            @app.route('/index/<arg1>/<arg2>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

            index(request=None)
    
    def test_arguments(self):
        app = WaffleApp('test')
        
        @app.route('/article/<name:str>')
        def article(request, name):
            return HTTPResponse(request, f"{name}")
            
        res = app.request(b'GET /article/test HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'test')
        
class requestTest(unittest.TestCase):
    def test_basic(self):
        app = WaffleApp('test')
        
        @app.route('/index')
        def index(request):
            return HTTPResponse(request, 'index')
            
        res = app.request(b'GET /index HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'index')
        
    def test_withArgs(self):
        app = WaffleApp('test')
        
        @app.route('/article/<name:str>')
        def article(request, name):
            return HTTPResponse(request, name)
            
        res = app.request(b'GET /article/test HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'test')
        
    def test_withMiddleware(self):
        app = WaffleApp('test', ['middleware.testMiddleware.TestMiddleware'])
        
        @app.route('/page')
        def page(request):
            return HTTPResponse(request, f'{request.META["middlewareHeader2"]}')
            
        res = app.request(b'GET /page HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'value')
        self.assertEqual(res.headers['middlewareHeader'], 'value')
        
    def test_404(self):
        app = WaffleApp('test')
        
        @app.route('/page')
        def page(request):
            return HTTPResponse(request, 'page')
            
        res = app.request(b'GET /existnt HTTP/1.1\r\n\r\n')
        self.assertEqual(res.statusCode, 404)
        
    def test_errorHandler(self):
        app = WaffleApp('test')
        
        @app.errorHandler(404)
        def handler(request):
            return HTTPResponse(request, '404')
            
        res = app.request(b'GET /existnt HTTP/1.1\r\n\r\n')
        self.assertEqual(res.content, b'404')