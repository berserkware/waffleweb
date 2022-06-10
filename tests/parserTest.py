import unittest

from waffleweb.files import File
from waffleweb.parser import parseBody, parseHeaders, parsePost
from waffleweb.request import Request

class ParsePostTest(unittest.TestCase):
    def test_urlencodedDataNormal(self):
        content = 'testData1=1234&testData2=567'
        postData = parsePost(content, 'application/x-www-form-urlencoded')[0]
        self.assertEqual(postData, {'testData1': '1234', 'testData2': '567'})
    
    def test_urlencodedDataOneValue(self):
        content = 'testData1=1234'
        postData = parsePost(content, 'application/x-www-form-urlencoded')[0]
        self.assertEqual(postData, {'testData1': '1234'})
    
    def test_formData(self):
        content = '----------------------------301008406445698181922656\r\nContent-Disposition: form-data; name="testData1"\r\n\r\n123\r\n----------------------------301008406445698181922656\r\nContent-Disposition: form-data; name="testData2"\r\n\r\n5678\r\n----------------------------301008406445698181922656--\r\n'
        postData = parsePost(content, 'multipart/form-data; boundary=--------------------------301008406445698181922656')[0]
        self.assertEqual(postData, {'testData1': '123', 'testData2': '5678'})
        
    def test_formDataWithFiles(self):
        content = '--12f2be4c4dbc55b5cfd9e23a63efe76e\r\nContent-Disposition: form-data; name="test"; filename="testFile.txt"\r\n\r\nTest Data lol\r\n--12f2be4c4dbc55b5cfd9e23a63efe76e--\r\n'
        postData = parsePost(content, 'multipart/form-data; boundary=12f2be4c4dbc55b5cfd9e23a63efe76e')[1]
        self.assertEqual(type(postData['test']), File)

class ParseBodyTest(unittest.TestCase):
    def test_bodyDataSpaces(self):
        req = 'POST / HTTP/1.1\r\nContent-Type: text/plain\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 102\r\n\r\nthis is some test body data for the body test becuase a book i read told me i should write more tests.'
        body = parseBody(req)
        self.assertEqual('\nthis is some test body data for the body test becuase a book i read told me i should write more tests.', body)
        
    def test_bodyDataNoSpaces(self):
        req = 'POST / HTTP/1.1\r\nContent-Type: text/plain\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nHost: localhost:8080\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 17\r\n\r\nmewhengettestdata'
        body = parseBody(req)
        self.assertEqual(body, '\nmewhengettestdata')

class ParseHeadersTest(unittest.TestCase):
    def test_headersData(self):
        req = 'GET /math/ HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nHost: localhost:8080\r\n\r\n'
        headers = parseHeaders(req)
        self.assertEqual(headers, {'USER_AGENT': 'PostmanRuntime/7.29.0', 'ACCEPT': '*/*', 'ACCEPT_ENCODING': 'gzip, deflate, br', 'CONNECTION': 'keep-alive', 'HOST': 'localhost:8080'})
        
    def test_headersDataWithBodyInRequest(self):
        req = 'GET /math/ HTTP/1.1\r\nUser-Agent: PostmanRuntime/7.29.0\r\nAccept: */*\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nHost: localhost:8080\r\n\r\ndummydata: test'
        headers = parseHeaders(req)
        self.assertEqual(headers, {'USER_AGENT': 'PostmanRuntime/7.29.0', 'ACCEPT': '*/*', 'ACCEPT_ENCODING': 'gzip, deflate, br', 'CONNECTION': 'keep-alive', 'HOST': 'localhost:8080'})