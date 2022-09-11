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

===================================================================================
``function waffleweb.request.matchVariableInURL(indexOfVar, urlVarData, splitUri)``
===================================================================================

This is used to match a part in a requested URL, to a URL variable in a view. It also converts the variable to the type. 
Returns a ``tuple`` with the name of the variable and the value: ('name', 'value').

**Parameters:**
 - **indexOfVar** (``int``) - The index of the part in the URL to convert.
 - **urlVarData** (``tuple``) - The name and type of the variable - ('name', 'type').
 - **splitUri** (``list``) - The split URI to match the variable to.

**Returns:** ``tuple``

================================================
``function waffleweb.request.findView(request)``
================================================

Finds the view function matching the URL and the URL variables in a dictionary, If a view matching the URL can't be found a ``HTTP404`` will be raised. Returns (view function, {'arg': argvalue, ... }).

**Parameters:**
 - **request** (``Request``) - The request to get find the view from.

**Returns:** ``tuple``

================================================================
``function waffleweb.request.getResponse(request, debug=False)``
================================================================

This function returns a response.

**Parameters:**
 - **request** (``Request``) - The request to get the data from.
 - **debug** (``bool``) (optional) - If debug mode is on.

**Returns:** ``HTTPResponse``