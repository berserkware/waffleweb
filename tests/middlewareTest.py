import unittest
import requests

class ProjectMiddlewareTest(unittest.TestCase):
    def test_before(self):
        pass

    def test_after(self):
        with requests.session() as s:
            res = s.get('http://localhost:8080/')
            resCookies = s.cookies
            self.assertEqual(resCookies.get_dict(), {'addedCookie': '32'})

class AppMiddlewareTest(unittest.TestCase):
    def test_beforeResponse(self):
        res = requests.get('http://localhost:8080/testBefore')
        self.assertEqual(res.content, b'{}')

    def test_afterResponse(self):
        res = requests.get('http://localhost:8080/')
        self.assertEqual(res.content, b'middlewareified')