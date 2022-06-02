import unittest
import requests

from waffleweb import WaffleApp

class basicRouteTest(unittest.TestCase):
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
        response = requests.get('http://localhost:8080/math/add/12/12').json()
        self.assertEqual(response, {'answer':24})


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

if __name__ == '__main__':
    unittest.main()