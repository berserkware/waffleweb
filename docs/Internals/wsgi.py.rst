=======
wsgi.py
=======

--------------------------------
``getResponseHeaders(response)``
--------------------------------

Gets the response headers is a list of tuples of names and values.

**Parameters:**
 - **response** (``HTTPResponse``) - The response to get the headers from.

**Returns:** ``list[tuple]``

-------------------------------
``getResponseStatus(response)``
-------------------------------

Gets the response status code and message.

**Parameters:**
 - **response** (``HTTPResponse``) - The response to get the status from.

**Returns:** ``str``