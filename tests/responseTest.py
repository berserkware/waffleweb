import unittest

import waffleweb.response as responses

class ResponseHeadersTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ResponseHeadersTest, self).__init__(*args, **kwargs)

        self.response = responses.ResponseHeaders("""
                                            200 OK
                                            Content-Type: text/html; charset=utf-8
                                            Content-Encoding: gzip
                                            """)

    def test_contentType(self):
        self.assertEqual(self.response['Content-Type'], 'text/html; charset=utf-8')

    def test_contentEncoding(self):
        self.assertEqual(self.response['Content-Encoding'], 'gzip')

class HTTPResponseBaseTest(unittest.TestCase):
    def test_contentTypeNotInHeaders(self):
        try:
            base = responses.HTTPResponseBase(contentType='text/html; charset=utf-8')
        except ValueError:
            self.fail('A value error was raised when initializing the HTTPResponseBase class')

    def test_contentTypeInHeaders(self):
        with self.assertRaises(ValueError):
            base = responses.HTTPResponseBase(headers='Content-Type: text/html; charset=utf-8', contentType='text/html; charset=utf-8')

    def test_NoContentTypeButInHeaders(self):
        try:
            base = responses.HTTPResponseBase(headers='Content-Type: text/html; charset=utf-8')
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
        response = responses.JSONResponse(jsonContent={'testJson': 1234})
        self.assertEqual(response.json, b'{"testJson": 1234}')

class FileResponseTest(unittest.TestCase):
    def test_file(self):
        with open('tests/commands.txt', 'rb') as f:
            response = responses.FileResponse(f, 'text/plain')

            self.assertEqual(response.fileObj, b"Run all tests:\r\npython3 -m unittest discover -s tests -p '*Test.py'\r\n")

    def test_mimeTypeNotNone(self):
        with open('tests/commands.txt', 'rb') as f:
            response = responses.FileResponse(f, 'text/plain')

            self.assertEqual(response.headers['Content-Type'], 'text/plain; charset=utf-8')

    def test_mimeTypeNone(self):
        with open('tests/commands.txt', 'rb') as f:
            response = responses.FileResponse(f)

            self.assertEqual(response.headers['Content-Type'], 'text/html; charset=utf-8')