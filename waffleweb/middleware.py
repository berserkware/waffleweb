from waffleweb.request import Request

def runRequestMiddleware(request: Request, middleware: list) -> Request:
    '''Runs all the middleware on the request'''

    for ware in middleware:
        #Trys to run the middleware's before function
        try:
            newRequest = ware.before(request)

            #Makes sure middleware returns Request object.
            if type(newRequest) == Request:
                request = newRequest
        except AttributeError:
            pass

    return request

def runResponseMiddleware(response, middleware: list):
    '''Runs all the middleware on the response'''
    
    for ware in middleware:
        #Trys to run the middleware's after function
        try:
            response = ware.after(response)
        except AttributeError:
            pass
    
    return response
