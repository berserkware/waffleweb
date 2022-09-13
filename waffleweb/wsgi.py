import waffleweb
from waffleweb.request import Request, getResponse
from waffleweb.middleware import runRequestMiddleware, runResponseMiddleware
from waffleweb.response import HTTPResponse
from waffleweb.exceptions import ParsingError
from waffleweb.errorResponses import badRequest

def getResponseHeaders(response) -> list[tuple]:
    """This gets the headers of a response. It puts headers into tuples, and then into a list."""

    responseHeaders = []

    headers = response.headers

    #gets the headers
    for key in headers.keys():
        if type(headers[key]) == list:
            for item in headers[key]:
                responseHeaders.append((key, str(item)))
        else:
            responseHeaders.append((key, str(headers[key])))

    return responseHeaders

def getResponseStatus(response) -> str:
    """This gets the code and status of a response, and puts it into a string"""
    return f'{response.statusCode} {response.reasonPhrase}'

def wsgiCallable(environ, startResponse):
    app = waffleweb.currentRunningApp

    #This gets the response.
    try:
        #Makes the Request object
        request = Request(environ, environ.get('REMOTE_ADDR'), True)

        request = runRequestMiddleware(request, app.middleware)

        response = getResponse(request)

        response = runResponseMiddleware(response, app.middleware)
    except ParsingError:
        response = badRequest(app, False)
    except:
        response = HTTPResponse(content='<title>500 Internal Server Error</title><h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">500</h1><h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">Internal Server Error.</h3>', status=500)

    #Gets the data
    content = response.content
    headers = getResponseHeaders(response)
    status = getResponseStatus(response)

    startResponse(status, headers)
    return iter([content])