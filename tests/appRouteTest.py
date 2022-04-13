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
    


if __name__ == '__main__':
    unittest.main()