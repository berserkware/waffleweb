import waffleweb

from waffleweb.response import HTTPResponse
from waffleweb.errorResponses import MethodNotAllowed, getErrorHandlerResponse

def handleHead(view, kwargs, request, debug: bool=False):
    #Checks if GET or HEAD is in allowed methods
    if 'GET' not in view.allowedMethods and 'HEAD' not in view.allowedMethods:
        #Returns 405 response if request method is not in the view's allowed methods
        res = getErrorHandlerResponse(errorHandlers=waffleweb.currentWorkingApp.errorHandlers, request=request, statusCode=405)
        if res is None:
            return MethodNotAllowed(view.allowedMethods, debug=debug)
        else:
            return res

    newView = view.view(request, **kwargs)

    newView.content = ''

    return newView

def handleOptions(view, request, debug: bool=False):
    #Checks if GET or OPTIONS is in allowed methods
    if 'GET' not in view.allowedMethods and 'OPTIONS' not in view.allowedMethods:
        #Returns 405 response if request method is not in the view's allowed methods
        res = getErrorHandlerResponse(errorHandlers=waffleweb.currentWorkingApp.errorHandlers, request=request, statusCode=405)
        if res is None:
            return MethodNotAllowed(view.allowedMethods, debug=debug)
        else:
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
        res = getErrorHandlerResponse(errorHandlers=waffleweb.currentWorkingApp.errorHandlers, request=request, statusCode=405)
        if res is None:
            return MethodNotAllowed(view.allowedMethods, debug=debug)
        else:
            return res

    return view.view(request, **kwargs)