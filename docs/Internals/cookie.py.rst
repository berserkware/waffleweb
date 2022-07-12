=========
cookie.py
=========

=================================================================================================================================
``class waffleweb.cookie.Cookie(name, value, path=None, maxAge=None, domain=None, secure=False, HTTPOnly=False, sameSite='Lax`)``
=================================================================================================================================

A Cookie. ``str()`` returns a string for the Set-Cookie header.

**Parameters:**
 - **name** (``str``) - The name of the cookie.
 - **value** (``str``) - The value of the cookie.
 - **path** (optional) (``str``) - The path of the cookie, defaults to the route of your app.
 - **maxAge**  (optional) (``str``) - The maximum age of the cookie.
 - **domain** (optional) (``str``) - The domain of the cookie.
 - **secure** (optional) (``bool``) - If the cookie is secure.
 - **HTTPOnly** (optional) (``bool``) - If the cookie is HTTP Only.
 - **sameSite** (optional) (``str``) - If your cookie is first-party of same-site.
 
=================================================================
``class waffleweb.cookie.Cookies(cookies=None, *args, **kwargs)``
=================================================================

Inherites from ``dict``

A special dictionary for cookies. ``str()`` returns a string of the cookies. For example: 'cookieName=value; cookieName2=value'.

**Parameters:**
 - **cookies** (``str``) - A string of all your the cookies. All of them get turned into ``Cookie`` objects. For example: 'cookieName=value; cookieName2=value'.