import unittest

import waffleweb.response as responses

class ResponseHeadersTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(responseHeadersTest, self).__init__(*args, **kwargs)

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
            base = responses.HttpResponseBase(status=1234)

    def test_statusTooSmall(self):
        with self.assertRaises(ValueError):
            base = responses.HTTPResponseBase(status=23)
