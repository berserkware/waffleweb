==========
request.py
==========

===============================================================
``class waffleweb.request.Request(rawRequest, IP, wsgi=False)``
===============================================================

A object for storing all the request data.

**Parameters:**
 - **rawRequest** (``bytes``) - The raw request.
 - **IP** (``str``) - The IP of the client sending the request.
 - **wsgi** (``bool``) - If the request is wsgi or not.
 
**Important attributes:**
 - **FILES** (``dict``) -  The uploaded files of the request.
 - **META** (``MultiValueOneKeyDict``) - The headers of the request.
 - **POST** (``dict``) - The POST data of the request.
 - **URL_PARAMS** (``dict``) - The URL parameters of the request.
 - **body** (``bytes``) - The body of the request.
 - **COOKIES** (``Cookies``) - All the request`s cookies.
 
------------------
``_getPostData()``
------------------

Parses and gets all the post and file data and adds them to the POST and FILES attributes.

**Returns:** ``None``

-------------------
``_getURLParams()``
-------------------

Gets all the URL parameters and adds them to the URL_PARAMS attribute.

**Returns:** ``None``

--------------
``_getBody()``
--------------

Parses and gets the body then returns it.

**Returns:** ``str``

-------------------
``property path()``
-------------------

Returns the URL of the request.

**Returns:** ``str``

---------------------
``property method()``
---------------------

Returns the HTTP method of the request.

**Returns:** ``str``

--------------------------
``property HTTPVersion()``
--------------------------

Returns the HTTP version of the request.

**Returns:** ``str``

===========================================================================
``class waffleweb.request.RequestHandler(request, debug=False, app=None)``
===========================================================================

A handler for requests to find the views and responses.

**Parameters:**
 - **request** (``Request``) - The Request to use to find the response.
 - **debug** (``bool``) - If debug mode is on.
 - **app** (``WaffleApp``) - A WaffleApp to get views from, instead of using the currently running app (``waffleweb.currentRunningApp``).
 
------------------------
``_getArg(index, part)``
------------------------

Converts the URL variable to it's type. Returns a ``tuple`` with the name of the variable and the value: ('name', 'value').

**Parameters:**
 - **index** (``int``) - The section in the URL to convert.
 - **part** (``list``) - The part in the view's URL to know what the type to convert is and the name of the argument.

**Returns:** ``tuple``

---------------
``_splitURL()``
---------------

Splits the request's URL into the different parts. Returns a ``tuple`` with the root, split root and extention: (root, splitRoot, ext).

**Returns:** ``tuple``

-------------
``findView()``
-------------

Finds the view function matching the URL and the URL variables in a dictionary, If a view matching the URL can't be found a ``HTTP404`` will be raised. Returns (view function, {view arguments}).

**Returns:** ``tuple``

-----------------------------
``_handleHead(view, kwargs)``
-----------------------------

Handles HEAD request by running the view functions with the kwargs and requests given then stripping the content. Returns what the matched view returns without the content.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends

--------------------------------
``_handleOptions(view, kwargs)``
--------------------------------

Handles OPTIONS request by basically ignores the view function and returning a response with all the allowed methods.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends

---------------------------------------
``_handleMethod(method, view, kwargs)``
---------------------------------------

Handles methods. If the ``method`` is HEAD, then it will return ``_handleHead()``. If the ``method`` is OPTIONS, then it will return ``_handleOptions()``. Any other method will just return what the view function returns.

**Parameters:**
 - **method** (``str``) - The method of the request.
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends
 
---------------------------------------------------
``getErrorHandlerResponse(response=None, statusCode=None)``
---------------------------------------------------

Looks for a error handler with the response's status code or the ``statusCode`` arg. If it finds an error handler it returns the response from the error handler otherwise it returns the ``response`` arg. You should provide either a response or a statusCode.

**Returns:** ``HTTPResponse``

**Parameters:**
 - **response** (optional) (``HTTPResponse``) - The response to get the status code from to find the handler.
 - **statusCode** (optional) (``int``) - The status code to find the handler.
 
--------------------
``_handle404View()``
--------------------

If a ``HTTP404`` is raised this function will get called. If debug is on it will return a default 404 error page. If debug is off then it will try to get a error handler, but if one cannot be found it will return a plain 404 page.

**Returns:** ``HTTPResponse``

----------------------------------------
``_405MethodNotAllowed(allowedMethods)``
----------------------------------------
If the view found does not allow the request's method then this will be called. If debug is on it will return a default 405 error page. If debug is off then it will try to get a error handler, but if one cannot be found it will return a plain 405 page.

**Returns:** ``HTTPResponse``

-----------------
``getResponse()``
-----------------

Gets a response.

**Returns:** ``HTTPResponse``