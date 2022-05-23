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

class RequestHeaderTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(RequestHeaderTest, self).__init__(*args, **kwargs)
        self.testRequest = testRequest

    def test_path(self):
        self.assertEqual(self.testRequest.path, '/')

    def test_method(self):
        self.assertEqual(self.testRequest.method, 'GET')
    
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

        self.assertEqual(handler._splitURL(), ('/page1/10/index', ['page1', '10', 'index'], ''))

    def test_methodNotAllowed(self):
        response = requests.get('http://localhost:8080/math/postTest')
        self.assertEqual(response.status_code, 405)

    def test_methodAllowed(self):
        response = requests.get('http://localhost:8080/math/add/1/1')
        self.assertEqual(response.status_code, 200)

    def test_methodNotImplemented(self):
        response = requests.delete('http://localhost:8080/math/add/1/1')
        self.assertEqual(response.status_code, 501)

    def test_handleGet(self):
        response = requests.get('http://localhost:8080/math/add/1/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'answer': 2})

    def test_handleHead(self):
        response = requests.head('http://localhost:8080/math/')
        self.assertEqual(response.status_code, 200)
        now = datetime.now(timezone('GMT'))
        dateTime = now.strftime("%a, %d %b %Y %X %Z")

        self.assertEqual(response.headers, {
            'Content-Type': 'text/html; charset=utf-8',
            'Date': dateTime,
            'Content-Length': '4',
            'Set-Cookie': 'addedCookie=32; path=/math/',
            })

    def test_handlePost(self):
        data = {'testData1': 15, 'testData2': 30}
        response = requests.post('http://localhost:8080/math/postTest/', data=data)
        self.assertEqual(response.content, b"{'testData1': '15', 'testData2': '30'}")