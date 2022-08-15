from waffleweb.errorResponses import badRequest, notImplementedError, pageNotFound
from waffleweb import WaffleApp
import unittest

from waffleweb.response import HTTPResponse

class BadRequestTest(unittest.TestCase):
    def test_debug(self):
        app = WaffleApp()

        self.assertEqual(badRequest(app, True).statusCode, 400)

    def test_noDebugNoHandler(self):
        app = WaffleApp()

        self.assertEqual(badRequest(app, False).content, b'400 Bad Request')

    def test_noDebugHandler(self):
        app = WaffleApp()

        @app.errorHandler(400)
        def badRequest():
            return HTTPResponse(content="handler content")

        self.assertEqual(badRequest().content, b'handler content')

class NotImplementedErrorTest(unittest.TestCase):
    def test_debugNoneResponse(self):
        app = WaffleApp()

        self.assertEqual(notImplementedError(None, True, 'GET').statusCode, 501)

    def test_debugResponse(self):
        app = WaffleApp()

        res = HTTPResponse(content='content') 
        self.assertEqual(notImplementedError(res, True, "GET").content, b'content')

    def test_noDebugNoneResponse(self):
        self.assertEqual(notImplementedError(None, False, "GET").content, b'Not Implemented Error')

    def test_noDebugResponse(self):
        res = HTTPResponse(content='response')
        self.assertEqual(notImplementedError(res, False, 'GET').content, b'response')
