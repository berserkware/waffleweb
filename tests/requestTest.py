from waffleweb.project import WaffleProject
from waffleweb.request import Request, RequestHandler

import unittest

from waffleweb.response import HTTP404

testRequest = Request("""GET / HTTP/1.1
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

class RequestHeaderTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RequestHeaderTest, self).__init__(*args, **kwargs)
        self.testRequest = testRequest

    def test_path(self):
        self.assertEqual(self.testRequest.path, '/')

    def test_method(self):
        self.assertEqual(self.testRequest.method, 'GET')
    
    def test_host(self):
        self.assertEqual(self.testRequest.headers['Host'], 'localhost:8080')

    def test_userAgent(self):
        self.assertEqual(self.testRequest.headers['User-Agent'], 'Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:96.0) Gecko/20100101 Firefox/96.0')

    def test_accept(self):
        self.assertEqual(self.testRequest.accept, 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')

    def test_acceptLangauge(self):
        self.assertEqual(self.testRequest.acceptLanguage, 'en-US,en;q=0.5')

    def test_acceptEncoding(self):
        self.assertEqual(self.testRequest.acceptEncoding, 'gzip, deflate')

    def test_connection(self):
        self.assertEqual(self.testRequest.connection, 'keep-alive')

    def test_cookie(self):
        self.assertEqual(self.testRequest.cookie, 'csrftoken=Db8QXnkjOLbPd3AGTxlnEEGTSn0IMh44MB8Pf2dVAPSBARoU6DteVUu9nT9ELqcO; sessionid=h8xln73emxlqgpjbsnx9007ceyfla7at')

    def test_clientIP(self):
        self.assertEqual(self.testRequest.clientIP, '101.98.137.19')

class RequestHandlerTest(unittest.TestCase):
    def test_splitURL(self):
        APPS = []

        request = Request("""GET /page1/10/index HTTP/1.1
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

        handler = RequestHandler(request, APPS)

        self.assertEqual(handler._splitURL(), ('page1/10/index', ['page1', '10', 'index'], ''))
