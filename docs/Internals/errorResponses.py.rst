=================
errorResponses.py
=================

==============================================================
``function waffleweb.errorResponses.badRequest(app, debug)``
==============================================================

It gets a 400 Bad Request response.

**Parameters:**
 - **apps** (``Request``) - The app to find the error handler.
 - **debug** (``bool``) - If the response should be debug.
 
**Returns:** ``HTTPResponse``

==================================================================================
``function waffleweb.errorResponses.notImplementedError(response, debug, method)``
==================================================================================

This will be called when the request's method is unknown this will be called. If debug is on it will return a default 501 error page. If debug is off then it will return the ``response``, but if the ``response`` is ``None`` it will return a plain 501 page.

**Parameters:**
 - **response** (``HTTPResponse``) - The response that the getErrorHandlerResponse method returns.
 - **debug** (``bool``) - If debug mode is on.
 - **method** (``str``) - The method that is not implemented.

**Returns:** ``HTTPResponse``

==========================================================================
``function waffleweb.errorResponses.pageNotFound(response, debug, views)``
==========================================================================

If a ``HTTP404`` is raised this function will get called in the request handler. If debug is on it will return a default 404 error page. If debug is off then it will use the ``response``, but if ``response`` is ``None`` it will return a plain 404 page.

**Paramters:**
 - **response** (``HTTPResponse``) - The response that the getErrorHandlerResponse method returns.
 - **debug** (``bool``) - If debug mode is on.
 - **views** (``list``) - The list of all the views to display for debug mode.

**Returns:** ``HTTPResponse``

=======================================================================================
``function waffleweb.errorResponses.methodNotAllowed(response, debug, allowedMethods)``
=======================================================================================

If the client sends a request with a method not allowed in your view, then this function will get called. If response is not None, then it will be returned, but if the response is None then a basic error page will be returned.

**Paramters:**
 - **response** (``HTTPResponse``) - The response that the getErrorHandlerResponse method returns.
 - **debug** (``bool``) - If debug mode is on.
 - **allowedMethods** (``list``) - The list of all the methods that are allowed.

**Returns:** ``HTTPResponse``

=============================================================================================
``getErrorHandlerResponse(errorHandlers=None, request=None, response=None, statusCode=None)``
=============================================================================================

Looks for a error handler with the response's status code or the ``statusCode`` arg. If it finds an error handler it returns the response from the error handler otherwise it returns the ``response`` arg. You should provide either a response or a statusCode.

**Returns:** ``HTTPResponse``

**Parameters:**
 - **errorHandlers** (optional) (``list[ErrorHandler]``) - The list of ErrorHandler's to find the responses from.
 - **request** (optional) (``Request``) - The request to pass to the error handling functions.
 - **response** (optional) (``HTTPResponse``) - The response to get the status code from to find the handler.
 - **statusCode** (optional) (``int``) - The status code to find the handler.