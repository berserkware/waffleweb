import unittest
from waffleweb.app import waffleApp

class basicRouteTest(unittest.TestCase):
    def test_pathInvalidRelitiveURL(self):
        app = waffleApp('test')

        with self.assertRaises(ValueError):
            @app.route('www.google.com', 'index')
            def index():
                pass    

            index()
    
    def test_pathValidRelitiveURL(self):
        app = waffleApp('test')
        try:
            @app.route('/home/index', 'index')
            def index():
                pass    

            index()
        except ValueError:
            self.fail('index() raised ValueError unexpectably')

    


if __name__ == '__main__':
    unittest.main()