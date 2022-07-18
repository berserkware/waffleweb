=============
middleware.py
=============

========================================================
``class waffleweb.middleware.Middleware(middleware=[])``
========================================================

This is a special list for storing middleware. It has special abilities that load middleware when middleware is appended or replaced. The middleware string have to be structured as so: 'module.MiddlewareClass'.

It has all the same methods as a list, except that it loads the middleware when you add them.

**Parameters:**
 - **middleware** (``list[str]``) - A list of all the middleware needed to be loaded. You need to format the middleware strings as so: 'module.MiddlewareClass'.

**Usage:**

.. code-block:: python

	from waffleweb.middleware import Middleware

	middleware = Middleware(['ware.TestMiddleware'])
	
	middleware.append('ware.OtherWare')
	middleware.append(['ware.One', 'ware.Two'])
	
	middleware[1] = 'ware.NewWare'

------------------------
``loadMiddleware(ware)``
------------------------

Loads the middleware into a dictionary. The dictionary include the module and the class of the middleware: ``{'module': middleware module, 'middleware': middlwareClass,}``.

=======================================================================
``class waffleweb.middleware.MiddlewareHandler(middleware)``
=======================================================================

A handler of middleware. Middleware gets ran on the request before your view receives it and on the response before it is sent.

**Parameters:**
 - **middleware** (``Middleware``) - A list of all your middleware.

--------------------------------------
``runRequestMiddleware(request)``
--------------------------------------

Runs all the middleware on the request and then returns the request. It calls the ``before(request)`` method on the middleware classes.

**Parameters:**
 - **request** (``Request``) - The request to run the middleware on.
 
**Returns:** ``Request``

----------------------------------------
``runResponseMiddleware(response, app)``
----------------------------------------

Runs all the middleware on the response and then returns the response. It calls the ``after(response)`` method on the middleware classes.

**Parameters:**
 - **request** (``HTTPResponse``) - The response to run the middleware on.
 
**Returns:** ``HTTPResponse``
