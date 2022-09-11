from waffleweb.response import HTTPResponse, JSONResponse, FileResponse
from waffleweb.errorResponses import methodNotAllowed, getErrorHandlerResponse

import waffleweb

def handleHead(view, kwargs, request, debug: bool=False):
    #Checks if GET or HEAD is in allowed methods
    if 'GET' not in view.allowedMethods and 'HEAD' not in view.allowedMethods:
        #Returns 405 response if request method is not in the view's allowed methods
        res = getErrorHandlerResponse(errorHandlers=waffleweb.currentRunningApp.errorHandlers, request=request, statusCode=405)
        return methodNotAllowed(res, debug, view.allowedMethods)

    newView = view.view(request, **kwargs)

    if type(newView) == HTTPResponse:
        newView.content = ''
    elif newView == JSONResponse:
        newView.json = {}
    elif newView == FileResponse:
        newView.fileObj = None

    return newView

def handleOptions(view, request, debug: bool=False):
    #Checks if GET or OPTIONS is in allowed methods
    if 'GET' not in view.allowedMethods and 'OPTIONS' not in view.allowedMethods:
        #Returns 405 response if request method is not in the view's allowed methods
        res = getErrorHandlerResponse(errorHandlers=waffleweb.currentRunningApp.errorHandlers, request=request, statusCode=405)
        return methodNotAllowed(res, debug, view.allowedMethods)

    if view is None:
        methods = ', '.join(['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'])
        res = HTTPResponse(status=204) 
        res.headers['Allow'] = methods
        return res
    
    allowedMethods = view.allowedMethods.copy()
    if 'GET' in allowedMethods:
        if 'HEAD' not in allowedMethods:
            allowedMethods.append('HEAD')
        if 'OPTIONS' not in allowedMethods:
            allowedMethods.append('OPTIONS')
    
    methods = ', '.join(allowedMethods)
    res = HTTPResponse(status=204) 
    res.headers['Allow'] = methods
    return res

def handleOther(view, kwargs, request, debug: bool=False):
    if request.method not in view.allowedMethods:
        #Returns 405 response if request method is not in the view's allowed methods
        res = getErrorHandlerResponse(errorHandlers=waffleweb.currentRunningApp.errorHandlers, request=request, statusCode=405)
        return methodNotAllowed(res, debug, view.allowedMethods)

    return view.view(request, **kwargs)