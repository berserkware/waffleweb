import waffleweb
import traceback

from waffleweb.response import HTTPResponse

class HTTPException(HTTPResponse):
    '''A class for HTTP exceptions.'''
    
    def __init__(
        self, 
        mainMessage, 
        subMessage='', 
        description='', 
        traceback='', 
        debug=False, 
        *args, 
        **kwargs
        ):
        super().__init__(*args, **kwargs)
        
        self.mainMessage = mainMessage
        self.subMessage = subMessage
        self.description = description
        self.traceback = traceback
        self.debug = debug
        
        if self.debug:
            self.content = self.debugErrorPage()
        else:
            self.content = self.errorPage()
        
    def debugErrorPage(self):
        if self.subMessage != '':
            subMessageSection = f'''
            <h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">{self.subMessage}</h2>
            '''
        else:
            subMessageSection = ''
        
        if self.description != '':
            contentSection = f'''
            <p style="color: #7a7a7a; display: block; margin:15px; padding:0px;">{self.description}</p>
            '''
        else:
            contentSection = ''
            
        if self.traceback != '':
            tracebackSection = f'''
            <fieldset style="display: block; margin:15px; padding:0px;">
                <legend style="margin-left:15px; margin-top:0px; margin-bottom:0px; padding:0px;"><h2 style="margin:0; padding:0px;">Traceback</h2></legend>
                <h3 style="margin-left:15px; margin-top:5px; margin-bottom:10px; padding:0px;">{self.traceback}</h3>
            </fieldset>
            '''
        else:
            tracebackSection = ''
        
        page = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{self.mainMessage}</title>
        </head>
        <body>
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">{self.mainMessage}</h1>
                {subMessageSection}
                {contentSection}
                {tracebackSection}
            </body>
        </body>
        </html>
        '''
        
        return page
        
    def errorPage(self):
        if self.subMessage != '':
            subMessageSection = f'''
            <h3 style="font-family: Arial, Helvetica, sans-serif; text-align: center; color: #5c5c5c; margin-top: 0px;">{self.subMessage}</h3>
            '''
        else:
            subMessageSection = ''
        
        page =  f'''
        <title>{self.mainMessage}</title>
        <h1 style="font-family: Arial, Helvetica, sans-serif; text-align: center; font-size: 80px; margin-bottom: 0px;">{self.mainMessage}</h1>
        {subMessageSection}
        '''
        return page

class BadRequest(HTTPException):
    '''A 400 Bad Request response'''
    
    def __init__(self, *args, **kwargs):
        super().__init__(
            mainMessage='400 Bad Request', 
            subMessage='The request was malformend so the server could not process it.', 
            *args, 
            **kwargs
            )
        
        self.statusCode = 400

class PageNotFound(HTTPException):
    '''A 404 Page Not Found Error response.'''
    
    def __init__(self, views, *args, **kwargs):
        #Gets all searched views.
        searchedViews = []
        for view in views:
            path = view.unstripedPath

            #turns the arrows into one html cannot render
            path = path.replace('<', '&lt;')
            path = path.replace('>', '&gt;')
            searchedViews.append(path)
        
        super().__init__(
            mainMessage='404 Not Found', 
            subMessage='The requested page could not be found', 
            traceback=f'Views searched:<br>{"<br>".join(searchedViews)}' ,
            *args, 
            **kwargs
            )

        self.statusCode = 404

class MethodNotAllowed(HTTPException):
    '''A Method Not Allow Response.'''
    
    def __init__(self, allowedMethods, *args, **kwargs):
        methods = ', '.join(allowedMethods)
        
        super().__init__(
            mainMessage='405 Method Not Allowed', 
            subMessage=f'Allowed Methods: {methods}', 
            *args, 
            **kwargs
            )
        
        self.headers['Allow'] = methods
        self.statusCode = 405

class InternalServerError(HTTPException):
    '''A Internal Server Error response.'''
    
    def __init__(self, exception: Exception, *args, **kwargs):
        #gets the exception
        tracebackException = traceback.TracebackException.from_exception(exception)
        
        splitTraceback = []
        #gets the traceback
        stack = tracebackException.stack.format()
        
        #For each line in the stack, format it, and add it to the list of
        #formatted stacklines.
        for stackLine in stack:
            stackLines = []
            
            #Gets the line number and code line
            splitStackLine = stackLine.split(', ')
            file = splitStackLine[0]
            lineNumber = splitStackLine[1]
            code = splitStackLine[2].strip('\n')
            
            #Gets the filePath line
            filePath = file.strip().split(' ')[1].strip('"')
            func = code.split(' ')[1].strip('\n').strip()
            stackLines.append(f'{filePath} in {func}():')

            lineNumber = lineNumber.split(' ')[1]
            code = stackLine.split('\n')[1]

            stackLines.append(f'{lineNumber}: {code}')

            splitTraceback.append(f'<code>{stackLines[0]}</code><br><div style="width: 100%; background-color: #d1d1d1;"><code style="margin-left: 15px; margin-top: 0px; margin-bottom: 0px;">{stackLines[1]}</code></div><br>')

        stackStr = '\n'.join(splitTraceback)

        if kwargs.get('debug', False):
            super().__init__(
                mainMessage=tracebackException.exc_type.__name__, 
                subMessage=str(exception), 
                traceback=stackStr, 
                *args, 
                **kwargs
                )
        else:
            super().__init__(
                mainMessage='500 Internal Server Error', 
                subMessage='Internal Server Error.', 
                *args, 
                **kwargs
                )

        self.statusCode = 500

def getErrorHandlerResponse(errorHandlers=None, request=None, response=None, statusCode=None):
    """Finds a error response, calls it, then returns the response."""

    if errorHandlers == None:
        errorHandlers = waffleweb.currentWorkingApp.errorHandlers

    #Goes through all the errorHandlers
    for handler in errorHandlers:
        try:
            #Checks to see if the handlers code is the same as the status Code
            if statusCode == handler.statusCode:
                return handler.view(request)
            #Checks to see the the response's status code is equal to the handlers code
            elif response.statusCode == handler.statusCode:
                return handler.view(request)
        except AttributeError:
            pass
    return response