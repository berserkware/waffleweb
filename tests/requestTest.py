from urllib import response
from pytz import timezone
from datetime import datetime
from waffleweb.project import WaffleProject
from waffleweb.request import Request, RequestHandler

import unittest
import requests

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
                        Sec-Fetch-User: ?1
                        
                        testContent1=12&testContent2=123
                        """, '101.98.137.19')

class RequestTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RequestTest, self).__init__(*args, **kwargs)
        self.request = Request('GET /math/ HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nCookie: addedCookie=32\r\nHost: localhost:8080\r\n\r\ntestData1=321&testData2=123', IP='127.0.0.1')

    def test_path(self):
        self.assertEqual(self.request.path, '/math/')

    def test_method(self):
        self.assertEqual(self.request.method, 'GET')

    def test_HTTPVersion(self):
        self.assertEqual(self.request.HTTPVersion, 'HTTP/1.1')

    def test_META(self):
        self.assertEqual(self.request.META,
            {
                'USER_AGENT': 'PostmanRuntime/7.29.0',
                'ACCEPT': '*/*',
                'ACCEPT_ENCODING': 'gzip, deflate, br',
                'CONNECTION': 'keep-alive',
                'COOKIE': 'addedCookie=32',
                'HOST': 'localhost:8080'
            }
        )

    def test_IP(self):
        self.assertEqual(self.request.IP, '127.0.0.1')

    def test_body(self):
        self.assertEqual(self.request.body, '\ntestData1=321&testData2=123')

    def test_FILES(self):
        with open('tests/static/test.html') as f:
            files = {'test': f}
            res = requests.post('http://localhost:8080/filesPostTest/', files=files)
            self.assertEqual(b'<h1>Testing Testing 123</h1>', res.content)