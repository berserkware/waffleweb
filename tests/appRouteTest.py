import unittest
from waffleweb import waffleApp

class basicRouteTest(unittest.TestCase):
    def test_pathInvalidRelitiveURL(self):
        app = waffleApp('test')

        with self.assertRaises(ValueError):
            @app.route('www.google.com', 'index')
            def index(request=None):
                pass    

            index()
    
    def test_pathValidRelitiveURL(self):
        app = waffleApp('test')
        try:
            @app.route('/home/index', 'index')
            def index(request=None):
                pass    

            index()
        except ValueError:
            self.fail('index() raised ValueError unexpectably')

    def test_getAllViews(self):
        app = waffleApp('test')

        @app.route('/index', 'index')
        def index(request=None):
            pass

        @app.route('/article', 'article')
        def article(request=None):
            pass

        self.assertEqual(app.views, [{'path': '/index', 'name': 'index'}, {'path': '/article', 'name': 'article'}])


    def test_getCheckIfArgumentsCorrect(self):
        app = waffleApp('test')

        @app.route('/index/<arg1:str>/<arg2:int>', 'index')
        def index(request, arg1, arg2):
            return (arg1, arg2)

        self.assertEqual(index(request=None), None)

    def test_argumentsFail(self):
        app = waffleApp('test')

        with self.assertRaises(TypeError):
            @app.route('/index/arg1:str>/<int:arg2>', 'index')
            def index(request, arg1, arg2):
                return (arg1, arg2) 

            index(request=None)

if __name__ == '__main__':
    unittest.main()