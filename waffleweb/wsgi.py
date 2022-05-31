from waffleweb.request import RequestHandler, Request
from waffleweb.response import HTTP404

class WsgiHandler:
    def __init__(self, environ, apps, middlewareHandler):
        self.apps = apps
        self.middlewareHandler = middlewareHandler

        #Makes the Request object
        request = Request(environ, environ.get('REMOTE_ADDR'), True)

        self.requestHandler = RequestHandler(request)

        view = None

        try:
            #Runs the request middleware
            view = self.requestHandler._getView()[0]

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
        cookiesToSet = self.response.cookiesToSet

        #Puts all the headers into tuples and adds them to the responseHeaders list
        for key in headers.keys():
            responseHeaders.append((key, headers[key]))

        #Puts all the cookiesToSet into tumples and adds them to the responseHeaders list
        for key in cookiesToSet.keys():
            responseHeaders.append(('Set-Cookie', str(cookiesToSet[key])))

        return responseHeaders

    def getResponseStatus(self):
        return f'{self.response.statusCode} {self.response.reasonPhrase}'