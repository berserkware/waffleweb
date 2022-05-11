import unittest
from waffleweb.request import Request
from waffleweb.response import render

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

class templateTest(unittest.TestCase):
    def test_renderWithoutContext(self):
        res = render(request, 'testWithoutContext.html')
        self.assertEqual(b'<h1>Testing Testing 1 2 3</h1>', res.content)

    def test_renderWithContext(self):
        res = render(request, 'testWithContext.html', {'testVar': 'Testing 1 2 3'})
        self.assertEqual(b'<h1>Testing Testing 1 2 3</h1>', res.content)
