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
