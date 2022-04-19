import unittest

import waffleweb.response as responses

class responseHeadersTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(responseHeadersTest, self).__init__(*args, **kwargs)

        self.response = responses.ResponseHeaders("""
                                            200 OK
                                            Content-Type: text/html; charset=utf-8
                                            Content-Encoding: gzip
                                            """)

    def test_contentType(self):
        self.assertEqual(self.response['Content-Type'], 'text/html; charset=utf-8')