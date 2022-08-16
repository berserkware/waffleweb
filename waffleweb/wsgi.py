from waffleweb.errorResponses import badRequest
from waffleweb.exceptions import ParsingError
from waffleweb.middleware import Middleware, runRequestMiddleware, runResponseMiddleware
from waffleweb.request import RequestHandler, Request
from waffleweb.response import HTTPResponse

class WsgiHandler:
    def __init__(self, environ, app, middleware: Middleware):
        self.app = app
        self.environ = environ
        self.middleware = middleware
        
    def getResponse(self):
        try:
            try:
                #Makes the Request object
                request = Request(self.environ, self.environ.get('REMOTE_ADDR'), True)
            except ParsingError:
                return badRequest(self.app, False)

            self.requestHandler = RequestHandler(request)

            request = runRequestMiddleware(request, self.middleware)

            self.requestHandler.request = request

            response = self.requestHandler.getResponse()

            response = runResponseMiddleware(response, self.middleware)

            self.response = response
        except:
            self.response = HTTPResponse(content='<title>500 Internal Server Error</title><h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">500</h1><h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">Internal Server Error.</h3>', status=500)

    def getResponseContent(self):
        return self.response.content

    def getResponseHeaders(self):
        responseHeaders = []

        headers = self.response.headers

        #gets the headers
        for key in headers.keys():
            if type(headers[key]) == list:
                for item in headers[key]:
                    responseHeaders.append((key, str(item)))
            else:
                responseHeaders.append((key, str(headers[key])))

        return responseHeaders

    def getResponseStatus(self):
        return f'{self.response.statusCode} {self.response.reasonPhrase}'
