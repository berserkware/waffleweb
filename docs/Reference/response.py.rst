===========
response.py
===========

=======================================================================================================
``class waffleweb.response.HTTPResponseBase(contentType=None, charset=None, status=None, reason=None)``
=======================================================================================================

Content Type is defaulted to 'text/html charset=charset'.

The Date header is automatically added.

The base for the responses.

**Parameters:**
 - **contentType** (optional) (``str``) - The content type of the response.
 - **charset** (optional) (``str``) - The charset to encode the response in, defaults to utf-8.
 - **status** (optional) (``int``) - The status code of the response, default is 200.
 - **reason** (optional) (``str``) - The reason phrase of the response.
 
**Important attributes:**
 - **headers** (`MultiValueOneKeyDict </Reference/datatypes.py.rst>`_) - A MultiValueOneKeyDict of all your headers.
 - **statusCode** (``int``) - The status code of the response.
 - **charset** (``str``) - The charset of the response.

---------------------------
``property reasonPhrase()``
---------------------------
The status reason phrase of the response, can be set but not deleted.

**Returns:** ``str``

----------------------
``property charset()``
----------------------
The charset of the response, can be set but not deleted.

**Returns:** ``str``

-------------------------------------------------------------------------------------------------------------
``setCookie(name, value, path=None, maxAge=None, domain=None, secure=False, HTTPOnly=False, sameSite='Lax')``
-------------------------------------------------------------------------------------------------------------

Sets a cookie to your response.

**Parameters:**
 - **name** (``str``) - The name of the cookie.
 - **value** (``str``) - The value of the cookie.
 - **path** (optional) (``str``) - The path of the cookie, defaults to the route of your app.
 - **maxAge**  (optional) (``str``) - The maximum age of the cookie.
 - **domain** (optional) (``str``) - The domain of the cookie.
 - **secure** (optional) (``bool``) - If the cookie is secure.
 - **HTTPOnly** (optional) (``bool``) - If the cookie is HTTP Only.
 - **sameSite** (optional) (``str``) - If your cookie is first-party of same-site.
 
**Returns:** ``None``
 
----------------------
``deleteCookie(name)``
----------------------

Deletes a cookie from your response.

**Parameters:**
 - **name** (``str``) - The name of your cookie.
 
**Returns:** ``None``

----------------------
``serializeHeaders()``
----------------------

Puts all the headers into a binary string.

**Returns:** ``bytes``

----------------------
``serialize(content)``
----------------------

This gets the fully binary string including headers and the content.

**Parameters:**
 - **content** (``str``) - The response content.

**Returns:** ``bytes``

-----------------------
``convertBytes(value)``
-----------------------

The converts the value to bytes, encoding is the response's charset.

**Parameters:**
 - **value** (``str``) - The value to convert.
 
=====================================================================================
``class waffleweb.response.HTTPResponse(request=None, content=b'', *args, **kwargs)``
=====================================================================================

Inherits from ``HTTPResponseBase``

A HTTP Response.

**Parameters:**
 - **request** (optional) (``Request``) - The request data for the cookies.
 - **content** (optional) (``str``) - The content of the response.
 
----------------------
``property content()``
----------------------

The content of the response, can be set but not deleted.

==========================================================================
``class waffleweb.response.JSONResponse(request=None, data={}, **kwargs)``
==========================================================================

Inherits from ``HTTPResponse``

A Json response.

**Parameters:**
 - **request** (optional) (``Request``) - The request data for the cookies.
 - **data** (optional) (``dict``) - The data of the response.
 
-------------------
``property data()``
-------------------

The data of the response, can be set but not deleted.

==============================================================================================
``class waffleweb.response.FileResponse(request=None, fileObj=None, mimeType=None, **kwargs)``
==============================================================================================

Inherits from ``HTTPResponse``

A file response.

**Parameters:**
 - **request** (optional) (``Request``) - The request data for the cookies.
 - **fileObj** (optional) (File object thing) - The file for the response.
 - **mimeType** (optional) (``str``) - The mime type of the response.
 
----------------------
``property fileObj()``
----------------------

The file of the response

===========================================================================
``class waffleweb.response.HTTPResponseRedirectBase(redirectTo, **kwargs)``
===========================================================================

Inherits from ``HTTPResponse``

The base for redirects.

**Parameters:**
 - **redirectTo** (``str``) - The URL to redirect to.
 
===================================================
``class waffleweb.response.HTTPResponseRedirect()``
===================================================

Inherits from ``HTTPResponseRedirectBase``

A redirect, status code is 302.

============================================================
``class waffleweb.response.HTTPResponsePermenentRedirect()``
============================================================

Inherits from ``HTTPResponseRedirectBase``

A permanent redirect, status code is 308.

=======================================================================================================================
``function waffleweb.response.render(request=None, filePath=None, context={}, charset=None, status=None, reason=None)``
=======================================================================================================================

Renders a template and returns a HTTPResponse. It uses `Jinja2 <https://palletsprojects.com/p/jinja/>`__ by default.

**Parameters:**
 - **request** (optional) (``Request``) - The request data for the cookies.
 - **filePath** (optional) (``str``) - The file path to your template.
 - **content** (optional) (``dict``) - The variables for your template.
 - **charset** (optional) (``str``) - The charset to encode the response in, defaults to utf-8.
 - **status** (optional) (``int``) - The status code of the response, default is 200.
 - **reason** (optional) (``str``) - The reason phrase of the response.

**Returns:** ``HTTPResponse``

=====================================================================
``function waffleweb.response.redirect(redirectTo, permanent=False)``
=====================================================================

A redirect.

**Parameters:**
 - **redirectTo** (``str``) - The URL to redirect to.
 - **permanent** (``bool``) - If the redirect is permanent.
 
**Returns:** ``HTTPResponseRedirect`` or ``HTTPResponsePermenentRedirect``
