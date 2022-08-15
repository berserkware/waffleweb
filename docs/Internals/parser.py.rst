=========
parser.py
=========

==========================================================
``function waffleweb.parser.parsePost(body, contentType)``
==========================================================

Parses post data and returns two dictionaries in a tuple: post data and files. It it cannot parse the data it will raise a ``ParsingError``.

**Parameters:**
 - **body** (``bytes``) - The body of the request.
 - **contentType** (``str``) - The content type of the request.
 
**Returns:** ``tuple[dict, dict]``

================================================
``function waffleweb.parser.parseBody(request)``
================================================

Takes a raw request and returns the body part of the request. It it cannot parse the data it will raise a ``ParsingError``.

**Parameters:**
 - **request** (``bytes``) - A raw request.
 
**Returns:** ``bytes``

===================================================
``function waffleweb.parser.parseHeaders(request)``
===================================================

Takes a raw request and returns a dictionary of the headers in string form. It it cannot parse the data it will raise a ``ParsingError``.

**Parameters:**
 - **request** (``bytes``) - A raw request.
 
**Returns:** ``dict``