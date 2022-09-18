from waffleweb.errorResponses import BadRequest, HTTPException, InternalServerError, PageNotFound, getErrorHandlerResponse, MethodNotAllowed
from waffleweb import WaffleApp
from waffleweb.request import Request
import unittest

from waffleweb.response import HTTPResponse

class HTTPExceptionTest(unittest.TestCase):
    def test_debugErrorPageOnlyMain(self):
        he = HTTPException('Main')
        expectedResult = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Main</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">Main</h1>
                
                
                
            </body>
        </body>
        </html>
        '''
        self.assertEqual(he.debugErrorPage(), expectedResult)
        
    def test_debugErrorPageSub(self):
        he = HTTPException('Main', 'Sub')
        expectedResult = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Main</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">Main</h1>
                
            <h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">Sub</h2>
            
                
                
            </body>
        </body>
        </html>
        '''
        self.assertEqual(he.debugErrorPage(), expectedResult)
        
    def test_debugErrorPageContent(self):
        he = HTTPException('Main', description='desc')
        expectedResult = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Main</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">Main</h1>
                
                
            <p style="color: #7a7a7a; display: block; margin:15px; padding:0px;">desc</p>
            
                
            </body>
        </body>
        </html>
        '''
        self.assertEqual(he.debugErrorPage(), expectedResult)
        
    def test_debugErrorPageTraceback(self):
        he = HTTPException('Main', traceback='traceback')
        expectedResult = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Main</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">Main</h1>
                
                
                
            <fieldset style="display: block; margin:15px; padding:0px;">
                <legend style="margin-left:15px; margin-top:0px; margin-bottom:0px; padding:0px;"><h2 style="margin:0; padding:0px;">Traceback</h2></legend>
                <h3 style="margin-left:15px; margin-top:5px; margin-bottom:10px; padding:0px;">traceback</h3>
            </fieldset>
            
            </body>
        </body>
        </html>
        '''
        self.assertEqual(he.debugErrorPage(), expectedResult)
        
    def test_debugErrorPageSubAndTraceback(self):
        he = HTTPException('Main', 'sub', traceback='traceback')
        expectedResult = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Main</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">Main</h1>
                
            <h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">sub</h2>
            
                
                
            <fieldset style="display: block; margin:15px; padding:0px;">
                <legend style="margin-left:15px; margin-top:0px; margin-bottom:0px; padding:0px;"><h2 style="margin:0; padding:0px;">Traceback</h2></legend>
                <h3 style="margin-left:15px; margin-top:5px; margin-bottom:10px; padding:0px;">traceback</h3>
            </fieldset>
            
            </body>
        </body>
        </html>
        '''
        self.assertEqual(he.debugErrorPage(), expectedResult)
        
    def test_errorPageOnlyMain(self):
        he = HTTPException('Main')
        expectedResult = f'''
        <title>Main</title>
        <h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">Main</h1>
        
        '''
        self.assertEqual(he.errorPage(), expectedResult)
        
    def test_errorPageWithSub(self):
        he = HTTPException('Main', 'Sub')
        expectedResult = f'''
        <title>Main</title>
        <h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">Main</h1>
        
            <h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">Sub</h3>
            
        '''
        self.assertEqual(he.errorPage(), expectedResult)

class BadRequestTest(unittest.TestCase):
    def test_debugErrorPage(self):
        he = BadRequest()
        expectedResult = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>400 Bad Request</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">400 Bad Request</h1>
                
            <h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">The request was malformend so the server could not process it.</h2>
            
                
                
            </body>
        </body>
        </html>
        '''
        self.assertEqual(he.debugErrorPage(), expectedResult)
        
    def test_errorPage(self):
        he = BadRequest()
        expectedResult = f'''
        <title>400 Bad Request</title>
        <h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">400 Bad Request</h1>
        
            <h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">The request was malformend so the server could not process it.</h3>
            
        '''
        self.assertEqual(he.errorPage(), expectedResult)
        
class PageNotFoundTest(unittest.TestCase):
    def test_debugErrorPage(self):
        he = PageNotFound([])
        expectedResult = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>404 Not Found</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">404 Not Found</h1>
                
            <h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">The requested page could not be found</h2>
            
                
                
            <fieldset style="display: block; margin:15px; padding:0px;">
                <legend style="margin-left:15px; margin-top:0px; margin-bottom:0px; padding:0px;"><h2 style="margin:0; padding:0px;">Traceback</h2></legend>
                <h3 style="margin-left:15px; margin-top:5px; margin-bottom:10px; padding:0px;">Views searched:<br></h3>
            </fieldset>
            
            </body>
        </body>
        </html>
        '''
        self.assertEqual(he.debugErrorPage(), expectedResult)
        
    def test_errorPage(self):
        he = PageNotFound([])
        expectedResult = f'''
        <title>404 Not Found</title>
        <h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">404 Not Found</h1>
        
            <h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">The requested page could not be found</h3>
            
        '''
        self.maxDiff = None
        self.assertEqual(he.errorPage(), expectedResult)
        
    def test_status(self):
        he = PageNotFound([])
        self.assertEqual(he.statusCode, 404)
        
class MethodNotAllowedTest(unittest.TestCase):
    def test_debugErrorPage(self):
        he = MethodNotAllowed(['GET', "POST"])
        expectedResult = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>405 Method Not Allowed</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">405 Method Not Allowed</h1>
                
            <h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">Allowed Methods: GET, POST</h2>
            
                
                
            </body>
        </body>
        </html>
        '''
        self.assertEqual(he.debugErrorPage(), expectedResult)
        
    def test_errorPage(self):
        he = MethodNotAllowed(['GET', 'POST'])
        expectedResult = f'''
        <title>405 Method Not Allowed</title>
        <h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">405 Method Not Allowed</h1>
        
            <h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">Allowed Methods: GET, POST</h3>
            
        '''

        self.assertEqual(he.errorPage(), expectedResult)
        
    def test_allowHeader(self):
        he = MethodNotAllowed(['GET', 'POST'])
        self.assertEqual(he.headers['Allow'], 'GET, POST')
        
    def test_status(self):
        he = MethodNotAllowed(['GET', 'POST'])
        self.assertEqual(he.statusCode, 405)
        
class InternalServerErrorTest(unittest.TestCase):
    def test_status(self):
        e = ValueError("Testing String")
        he = InternalServerError(e)
        self.assertEqual(he.statusCode, 500)
        
    def test_errorPage(self):
        e = ValueError("Testing String")
        he = InternalServerError(e)
        expectedResult = f'''
        <title>500 Internal Server Error</title>
        <h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">500 Internal Server Error</h1>
        
            <h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">Internal Server Error.</h3>
            
        '''

        self.assertEqual(he.errorPage(), expectedResult)
        
class GetErrorHandlerResponseTest(unittest.TestCase):
    def test_getErrorHandlerResponseByResponse(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        res = getErrorHandlerResponse(request=request, response=HTTPResponse(request, 'test', status=220))
        
        self.assertEqual(res.content, b'220 Page')
        
    def test_getErrorHandlerResponseByStatus(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        res = getErrorHandlerResponse(request=request, statusCode=220)
        
        self.assertEqual(res.content, b'220 Page')
        
    def test_getErrorHandlerResponseStatusNoHandler(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )

        res = getErrorHandlerResponse(request=request, statusCode=223)
        
        self.assertEqual(res, None)
        
    def test_getErrorHandlerResponseByResponseNoHandler(self):
        request = Request(
            b'GET /statusNoHandler HTTP/1.1\r\n\r\n', 
            '101.98.137.19'
            )
        res = HTTPResponse(request, 'test', status=223)
        errorHandler = getErrorHandlerResponse(request=request, response=res)
        
        self.assertEqual(errorHandler.content, res.content)
