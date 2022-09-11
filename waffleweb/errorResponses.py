import waffleweb
from waffleweb.response import HTTPResponse
from waffleweb.template import renderErrorPage

def badRequest(app, debug):
    '''Returns a 400 Bad Request response'''

    if debug == False:
        for handler in app.errorHandlers:
            try:
                if handler.statusCode == 400:
                    return handler.view()
            except AttributeError:
                pass
                
        return HTTPResponse(content='400 Bad Request', status=400)
    else:
        render = renderErrorPage('400 Bad Request', subMessage='The request was malformend so the server could not process it.')
        return HTTPResponse(content=render, status=400)

def notImplementedError(response, debug, method):
    '''Returns a 501 Not Implemented Error response.'''

    if debug:
        if response == None:
            render = renderErrorPage(
                mainMessage='501 Not Implemented Error', 
                subMessage=f'The requested method is not implemented',
                traceback=f'Method:{method}',
            )
            return HTTPResponse(content=render, status=501) 
        else:
            return response
    else:
        if response == None:
            return HTTPResponse(content='Not Implemented Error', status=501)
        else:
            return response

def pageNotFound(response, debug, views):
    '''Returns a 404 Page Not Found Error response.'''

    if debug:
        if response is None:
            #Gets all searched views.
            searchedViews = []
            for view in views:
                path = view.unstripedPath

                #turns the arrows into one html cannot render
                path = path.replace('<', '&lt;')
                path = path.replace('>', '&gt;')
                searchedViews.append(path)

            page = renderErrorPage(
                mainMessage='404 Page Not Found', 
                subMessage=f'The requested page could not be found',
                traceback=f'Views searched:<br>{"<br>".join(searchedViews)}',
                )
            return HTTPResponse(content=page, status=404)
        else:
            return response
    else:
        if response is None:
            return HTTPResponse(content='<title>404 Not Found</title><h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">404</h1><h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">The requested page could not be found.</h3>', status=404)
        else:
            return response

def methodNotAllowed(response, debug, allowedMethods):
    methods = ', '.join(allowedMethods)
    if debug:
        if response == None:
            render = renderErrorPage(
                mainMessage='405 Method Not Allowed',
                subMessage=f'Allowed Methods: {methods}',
            )
            res = HTTPResponse(content=render, status=405) 
            res.headers['Allow'] = methods
            return res
        else:
            return response
    else:
        if response == None:
            res = HTTPResponse(content='405 Method not Allowed', status=405) 
            res.headers['Allow'] = methods
            return res
        else:
            return response

def getErrorHandlerResponse(errorHandlers=None, request=None, response=None, statusCode=None):
    """Finds a error response, calls it, then returns the response."""

    if errorHandlers == None:
        errorHandlers = waffleweb.currentRunningApp.errorHandlers

    #Goes through all the errorHandlers
    for handler in errorHandlers:
        try:
            #Checks to see if the handlers code is the same as the status Code
            if handler.statusCode == statusCode:
                return handler.view(request)
            #Checks to see the the response's status code is equal to the handlers code
            elif response.statusCode == handler.statusCode:
                return handler.view(request)
        except AttributeError:
            pass
    return response