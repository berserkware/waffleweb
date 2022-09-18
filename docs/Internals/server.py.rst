=========
server.py
=========

=======================================================================================
``class waffleweb.server.WaffleServer(getResponseFunc, raw=False, runMiddleware=True)``
=======================================================================================

This is a webserver made to be easily customizable. This webserver
should not be used in production as it does not have proper 
security. 

**Parameters:**
 - **getResponseFunc** (``function``) - The function that gets the response to return to the client. Your function should take a ``Request`` object if raw is False, but if ``raw`` is True, the function  should take a ``bytes`` string. Your function should also take a ``debug`` parameter. ``getResponseFunc`` is called whenever a request comes in.
 - **raw** (``bool``) - This parameter dictates if a ``bytes`` string or a ``Request`` object is passed to the ``getResponseFunc``.
 - **runMiddleware** (``bool``) - If the middleware should be run on the request and the response. If ``raw`` and is on then middleware won't be run on requests.