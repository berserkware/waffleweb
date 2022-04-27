import unittest
from waffleweb.static import StaticHandler
from waffleweb.response import HTTP404, FileResponse

class StaticHandlerTest(unittest.TestCase):
    def test_findFile(self):
        handler = StaticHandler('testCSS', ['cssTest'], '.css')
        self.assertEqual(type(handler.findFile()), FileResponse)

    def test_findFileDoesntExist(self):
        handler = StaticHandler('DoesntExist', ['DoesntExist'], '.jpg')
        with self.assertRaises(HTTP404):
            handler.findFile()

    def test_findFileMimeKnown(self):
        handler = StaticHandler('testCSS', ['cssTest'], '.css')
        response = handler.findFile()
        self.assertEqual(response.mimeType, 'text/css')

    def test_findFileMimeUnknown(self):
        handler = StaticHandler('unknownmine', ['unknownmine'], '.whateveredoo')
        response = handler.findFile()
        self.assertEqual(response.mimeType, 'application/octet-stream')