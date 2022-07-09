import unittest

from waffleweb.app import WaffleApp

from waffleweb.request import Request
import waffleweb.response as responses
from waffleweb.datatypes import MultiValueOneKeyDict

request = Request(b"""GET /page1/10/index HTTP/1.1
                        Host: localhost:8080
                        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:96.0) Gecko/20100101 Firefox/96.0
                        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
                        Accept-Language: en-US,en;q=0.5
                        Accept-Encoding: gzip, deflate
                        Connection: keep-alive
                        Cookie: csrftoken=Db8QXnkjOLbPd3AGTxlnEEGTSn0IMh44MB8Pf2dVAPSBARoU6DteVUu9nT9ELqcO; sessionid=h8xln73emxlqgpjbsnx9007ceyfla7at
                        Upgrade-Insecure-Requests: 1
                        Sec-Fetch-Dest: document
                        Sec-Fetch-Mode: navigate
                        Sec-Fetch-Site: none
                        Sec-Fetch-User: ?1""", '101.98.137.19')

class HTTPResponseBaseTest(unittest.TestCase):
    def test_contentTypeNotInHeaders(self):
        try:
            base = responses.HTTPResponseBase(contentType='text/html; charset=utf-8')
        except ValueError:
            self.fail('A value error was raised when initializing the HTTPResponseBase class')

    def test_charsetNone(self):
        base = responses.HTTPResponseBase()

        self.assertEqual(base.charset, 'utf-8')

    def test_charset(self):
        base = responses.HTTPResponseBase(charset='ascii')

        self.assertEqual(base.charset, 'ascii')

    def test_statusString(self):
        with self.assertRaises(TypeError):
            base = responses.HTTPResponseBase(status='testastring')

    def test_statusTooBig(self):
        with self.assertRaises(ValueError):
            base = responses.HTTPResponseBase(status=1234)

    def test_statusTooSmall(self):
        with self.assertRaises(ValueError):
            base = responses.HTTPResponseBase(status=23)

    def test_statusJustRight(self):
        try:
            base = responses.HTTPResponseBase(status=250)
        except ValueError:
            self.fail('A ValueError was raised when initializing the HTTPResponseBase class')

    def test_reasonPhraseCorrect(self):
        base = responses.HTTPResponseBase(status=404)
        self.assertEqual(base.reasonPhrase, 'Not Found')

    def test_reasonPhraseCustom(self):
        base = responses.HTTPResponseBase(status=200, reason='tis ok')
        self.assertEqual(base.reasonPhrase, 'tis ok')

    def test_reasonPhraseUnknown(self):
        base = responses.HTTPResponseBase(status=220)
        self.assertEqual(base.reasonPhrase, 'Unknown status code.')

    def test_reasonPhraseUnknownButGivenReason(self):
        base = responses.HTTPResponseBase(status=220,  reason='i do not know the status code')
        self.assertEqual(base.reasonPhrase, 'i do not know the status code')

    def test_charsetGiven(self):
        base = responses.HTTPResponseBase(charset='ascii')
        self.assertEqual(base.charset, 'ascii')

    def test_charsetDefault(self):
        base = responses.HTTPResponseBase()
        self.assertEqual(base.charset, 'utf-8')

    def test_convertBytesStr(self):
        base = responses.HTTPResponseBase()
        self.assertEqual(base.convertBytes('Testing 1 2 3'), b'Testing 1 2 3')

class HTTPResponseTest(unittest.TestCase):
    def test_content(self):
        response = responses.HTTPResponse(content='Test content for tests')
        self.assertEqual(response.content, b'Test content for tests')

class JSONResponseTest(unittest.TestCase):
    def test_json(self):
        response = responses.JSONResponse(data={'testJson': 1234})
        self.assertEqual(response.data, b'{"testJson": 1234}')

class FileResponseTest(unittest.TestCase):
    def test_file(self):
        with open('tests/commands.txt', 'rb') as f:
            response = responses.FileResponse(request, f, 'text/plain')

            self.assertEqual(response.fileObj, b"Run all tests:\r\npython3 -m unittest discover -s tests -p '*Test.py'\r\n")

    def test_mimeTypeNotNone(self):
        with open('tests/commands.txt', 'rb') as f:
            response = responses.FileResponse(request, f, 'text/plain')

            self.assertEqual(response.headers['Content-Type'], 'text/plain; charset=utf-8')

    def test_mimeTypeNone(self):
        with open('tests/commands.txt', 'rb') as f:
            response = responses.FileResponse(request, f)

            self.assertEqual(response.headers['Content-Type'], 'text/plain; charset=utf-8')

class HTTPResponseRedirectTest(unittest.TestCase):
    def test_redirect(self):
        app = WaffleApp('testApp')
        
        @app.route('redirecternator')
        def redirectTest(request):
            return responses.HTTPResponseRedirect('/page')
            
        res = app.request(b'GET /redirecternator HTTP/1.1\r\n\r\n')
        
        self.assertEqual(res.headers['Location'], '/page')