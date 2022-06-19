import unittest
from waffleweb.request import Request
from waffleweb.static import getStaticFileResponse, findStatic
from waffleweb.response import HTTP404, FileResponse

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

class StaticHandlerTest(unittest.TestCase):
    def test_findFile(self):
        res = getStaticFileResponse(request, 'testCSS', '.css')
        self.assertEqual(type(res), FileResponse)

    def test_findFileDoesntExist(self):
        with self.assertRaises(HTTP404):
            res = getStaticFileResponse(request, 'DoesntExist', '.jpg')

    def test_findFileMimeKnown(self):
        response = getStaticFileResponse(request, 'testCSS', '.css')
        self.assertEqual(response.mimeType, 'text/css')

    def test_findFileMimeUnknown(self):
        response = getStaticFileResponse(request, 'unknownmine', '.whateveredoo')
        self.assertEqual(response.mimeType, 'application/octet-stream')

class FindStaticTest(unittest.TestCase):
    def test_findStaticContent(self):
        with findStatic('test.html', 'r') as f:
            file = f.read()
            self.assertEqual(file, '<h1>Testing Testing 123</h1>')