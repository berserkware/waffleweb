=============
middleware.py
=============

===========================================================================
``function waffleweb.middleware.runRequestMiddleware(request, middleware)``
===========================================================================

Runs all the middleware on the request and then returns the request. It calls the ``before(request)`` method on the middleware classes.

**Parameters:**
 - **request** (``Request``) - The request to run the middleware on.
 - **middleware** (``Middleware``) - The middleware to run on the request.
 
**Returns:** ``Request``

=============================================================================
``function waffleweb.middleware.runResponseMiddleware(response, middleware)``
=============================================================================

Runs all the middleware on the response and then returns the response. It calls the ``after(response)`` method on the middleware classes.

**Parameters:**
 - **response** (``HTTPResponse``) - The response to run the middleware on.
 - **middleware** (``Middleware``) - The middleware to run on the request.
 
**Returns:** ``HTTPResponse``
