import unittest

from waffleweb import WaffleApp
from waffleweb.response import HTTPResponse
from waffleweb.app import View
class ViewTest(unittest.TestCase):
    def test_hasPathHasArgsNoArgs(self):
        view = View(
            '/this/is/<test:int>',
            'this/is/<test:int>',
            ['this', 'is', ['test', 'int']],
            'testTo',
            None,
            ['GET'],
            )
            
        self.assertTrue(view.hasPathHasArgs())
        
    def test_hasPathHasArgsYesArgs(self):
        view = View(
            '/this/is/atest',
            'this/is/atest',
            ['this', 'is', 'test'],
            'testTo',
            None,
            ['GET'],
            )
            
        self.assertFalse(view.hasPathHasArgs())

class WaffleAppRouteVariablesTest(unittest.TestCase):
    def test_urlVariablesFail(self):
        app = WaffleApp()

        with self.assertRaises(AttributeError):
            @app.route('/index/arg1:str>/<int:arg2>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

    def test_urlVariablesRaiseAttributeError(self):
        app = WaffleApp()
        with self.assertRaises(AttributeError):
            @app.route('/index/<arg1:int>/<arg2:notAValidType>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

    def test_urlVariablesRaiseAttributeError2(self):
        app = WaffleApp()
        
        with self.assertRaises(AttributeError):
            @app.route('/index/<arg1>/<arg2>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 
    
    def test_urlVariablesNoValues(self):
        app = WaffleApp()
        
        with self.assertRaises(AttributeError):
            @app.route('/index/<>/<>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 
                
    def test_urlVariablesCorrect(self):
        app = WaffleApp()
        
        try:
            @app.route('/index/<arg1:int>/<arg2:int>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 
        except AttributeError:
            self.fail('A AttributeError was raised, even though everything is correct.')
     
class WaffleAppRoutePath(unittest.TestCase):
    def test_pathInvalidRelitiveURL(self):
        app = WaffleApp()

        with self.assertRaises(ValueError):
            @app.route('www.google.com', 'index')
            def index(request=None):
                pass    
    
    def test_pathValidRelitiveURL(self):
        app = WaffleApp()
        
        try:
            @app.route('/home/index', 'index')
            def index(request=None):
                pass    
            
        except ValueError:
            self.fail('index() raised ValueError unexpectably')
            
class WaffleAppRouteViewCreation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        app = WaffleApp()
        
        @app.route('/test/<arg:int>', 'testPage', ['GET', 'POST'])
        def func(request, arg):
            return HTTPResponse(request)
            
        self.func = func
            
        #Gets the latest view added
        self.view = app.views[-1]
        
    def test_unstripedPathCorrect(self):
        self.assertEqual(self.view.unstripedPath, '/test/<arg:int>')
        
    def test_pathCorrect(self):
        self.assertEqual(self.view.path, 'test/<arg:int>')
        
    def test_splitPathCorrect(self):
        self.assertEqual(self.view.splitPath, ['test', ['arg', 'int']])
        
    def test_nameCorrectExplicitNaming(self):
        self.assertEqual(self.view.name, 'testPage')
        
    def test_nameCorrectFromFunction(self):
        app = WaffleApp()
        
        @app.route('/test/<arg:int>', methods=['GET', 'POST'])
        def func(request, arg):
            return HTTPResponse(request)
        
        self.assertEqual(app.views[-1].name, 'func')
        
    def test_allowedMethodsCorrect(self):
        self.assertEqual(self.view.allowedMethods, ['GET', 'POST'])
        
class WaffleAppErrorHandlerTest(unittest.TestCase):
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
            
    def test_statusNotANumber(self):
        with self.assertRaises(TypeError):
            app = WaffleApp()
            
            @app.errorHandler("notANum")
            def handler(request):
                return HTTPResponse(request, '404')