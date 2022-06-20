======
app.py
======

=====================================================
``class waffleweb.WaffleApp(appName, middleware=[])``
=====================================================

The WaffleApp object is what you attach your views and app specific middleware to.

**Parameters:**
 - **appName** (``str``) - The name of your app.
 - **middleware** (``list[str]``) - A list of your app's middleware. All the middleware are strings with the module and middleware class. Example: 'testModule.Middleware' or 'middleware.testModule.Middleware'.

---------------------------------------------------------------------------------------------------------------
``route(path='/', name=None, methods=['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT'])``
---------------------------------------------------------------------------------------------------------------

A decorator to route a function to an URL.

**Parameters:**
 - **path** (``str``) - The path to your view.
 - **name** (``str``) - The name of your view.
 - **methods** (``list[str]``) - The allowed methods for your view.
 
----------------------------
``errorHandler(statusCode)``
----------------------------

A decorator to route a function to a certain error code. Whenever your return a response with a status code, if you have a errorHandler with that status code it will return your errorHandler.

**Parameters:**
 - **statusCode** (``int``) - The status code to route the function to.
