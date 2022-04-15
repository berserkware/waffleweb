from waffleweb import Request

import unittest

class headerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(headerTest, self).__init__(*args, **kwargs)
        self.testRequest = Request("""GET / HTTP/1.1\n
                        Host: localhost:8080\n
                        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:96.0) Gecko/20100101 Firefox/96.0\n
                        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\n
                        Accept-Language: en-US,en;q=0.5\n
                        Accept-Encoding: gzip, deflate\n
                        Connection: keep-alive\n
                        Cookie: csrftoken=Db8QXnkjOLbPd3AGTxlnEEGTSn0IMh44MB8Pf2dVAPSBARoU6DteVUu9nT9ELqcO; sessionid=h8xln73emxlqgpjbsnx9007ceyfla7at\n
                        Upgrade-Insecure-Requests: 1\n
                        Sec-Fetch-Dest: document\n
                        Sec-Fetch-Mode: navigate\n
                        Sec-Fetch-Site: none\n
                        Sec-Fetch-User: ?1\n""", '101.98.137.19')



    def test_path(self):
        self.assertEqual(self.testRequest.path, '/')