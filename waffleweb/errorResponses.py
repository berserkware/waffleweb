from waffleweb.response import HTTPResponse
from waffleweb.template import renderErrorPage

def badRequest(app, debug):
    if debug == False:
        for handler in app.errorHandlers:
            try:
                if handler.statusCode == 400:
                    return bytes(handler.view())
            except AttributeError:
                pass
                
        return bytes(HTTPResponse(content='400 Bad Request', status=400))
    else:
        render = renderErrorPage('400 Bad Request', subMessage='The request was malformend so the server could not process it.')
        return bytes(HTTPResponse(content=render, status=400))