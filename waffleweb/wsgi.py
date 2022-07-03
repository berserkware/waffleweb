from waffleweb.errorResponses import badRequest
from waffleweb.exceptions import ParsingError
from waffleweb.request import RequestHandler, Request
from waffleweb.response import HTTP404, HTTPResponse

class WsgiHandler:
    def __init__(self, environ, apps, middlewareHandler):
        self.apps = apps
        self.environ = environ
        self.middlewareHandler = middlewareHandler
        
    def getResponse(self):
        try:
            #Makes the Request object
            request = Request(self.environ, self.environ.get('REMOTE_ADDR'), True)
        except ParsingError:
            return badRequest(self.apps, False)

        self.requestHandler = RequestHandler(request)

        view = None

        try:
            #Runs the request middleware
            view = self.requestHandler.getView()[0]

            request = self.middlewareHandler.runRequestMiddleware(request, view)
        except HTTP404:
            pass

        self.requestHandler.request = request

        response = self.requestHandler.getResponse()

        if view is not None:
            #Run middleware on response
            response = self.middlewareHandler.runResponseMiddleware(response, view)

        self.response = response

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