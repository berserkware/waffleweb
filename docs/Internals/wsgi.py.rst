=======
wsgi.py
=======

======================================================================
``class waffleweb.wsgi.WsgiHandler(environ, app, middlewareHandler)``
======================================================================

Handles WSGI.

**Parameters:**
 - **environ** (``dict``) - The environ with all the request data and stuff as outlined in PEP 3333.
 - **app** (``WaffleApp``) - The WaffleApp of your web application.
 - **middlewareHandler** (``MiddlewareHandler``) - The middleware handler for middleware.

-----------------
``getResponse()``
-----------------

Gets the response and runs the middleware on it and sets the attribute 'response' to the response.

**Returns:** ``None``

------------------------
``getResponseContent()``
------------------------

Gets the content of the response

**Returns:** ``bytes``

------------------------
``getResponseHeaders()``
------------------------

Gets the response headers is a list of tuples of names and values.

**Returns:** ``list[tuple]``

-----------------------
``getResponseStatus()``
-----------------------

Gets the response status code and message.

**Returns:** ``str``