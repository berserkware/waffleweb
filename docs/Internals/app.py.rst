======
app.py
======

===============================
``class waffleweb.WaffleApp()``
===============================

The WaffleApp object is the center of your web application.

---------------------------------------------------------------------------------------------------------------
``route(path='/', name=None, methods=['GET'])``
---------------------------------------------------------------------------------------------------------------

A decorator to route a function to an URL.

**Parameters:**
 - **path** (``str``) - The path to your view.
 - **name** (``str``) - The name of your view.
 - **methods** (``list[str]``) - The allowed methods for your view.
 
----------------------------
``errorHandler(statusCode)``
----------------------------

A decorator to route a function to a certain error code. Whenever you return a response with a status code a errorHandler will be looked for with that status code. it will return your errorHandler.

**Parameters:**
 - **statusCode** (``int``) - The status code to route the function to.

-----------------------
``request(rawRequest)``
-----------------------

Sends a request to any of the views. It's main use is for the testing of waffleweb. It goes through the normal process that the requests takes when going through the server, except it doesn't go through a server.

**Parameters:**
 - **rawRequest** (``bytes``) - A byte request.
 
**Returns:** Response
 
**Usage:**

.. code-block:: python

	from waffleweb import WaffleApp
	
	app = WaffleApp('appName')
	
	@app.route('/')
	def index(request):
	    return HTTPResponse(request, 'index')
	    
	res = app.request(b'GET /index HTTP/1.1\r\nHeader-Name: value\r\n\r\n')
	
-------------------------------------------------
``run(host='127.0.0.1', port=8000, debug=False)``
-------------------------------------------------

Runs a test server. This shouldn't be used in production as it does not have any security checks.

**Parameters:**
 - **host** (optional) (``str``) - The host of your website.
 - **port** (optional) (``int``) - The port of your website.
 - **debug** (optional) (``bool``) - If your server is in debug mode.

**Returns:** ``None``

-------------------------------------------
``wsgiApplication(environ, startResponse)``
-------------------------------------------

A WSGI application. As outlined in `PEP 3333 <https://peps.python.org/pep-3333/>`_.

**Parameters:**
 - **environ** (``dict``) - For your wsgi server gateway. As outlined in `PEP 3333 <https://peps.python.org/pep-3333/>`_.
 
 - **startResponse** (``func``) - For your wsgi server gateway. As outlined in `PEP 3333 <https://peps.python.org/pep-3333/>`_.
 
**Returns:** ``iter()``

======================================================================================================================
``class waffleweb.app.View(unstripedPath=None, path=None, splitPath=None, name=None, view=None, allowedMethods=None)``
======================================================================================================================

A class to store views.

**Parameters:**
 - **unstripedPath** (optional) (``str``) - The unstriped, raw path of the view.
 - **path** (optional) (``str``) - The striped path of the view. The slashes are striped off the path.
 - **splitPath** (optional) (``list``) - The path split by slashes.
 - **name** (optional) (``str``) - The name of the view.
 - **view** (optional) (``func``) - The view function.
 - **allowedMethods** (optional) (``list``) - The allowed methods of the view.
 
--------------------
``hasPathHasArgs()``
--------------------
Checks whether or not the path of the view has variables in it.
 
======================================================
``class waffleweb.app.ErrorHandler(statusCode, view)``
======================================================

A class to store error handlers.

**Parameters:**
 - **statusCode** (optional) (``int``) - The status code that the handler handles.
 - **view** (optional) (``func``) - The view function.