=================
methodHandler.py
=================

===================================================================================
``function waffleweb.methodHandler.handleHead(view, kwargs, request, debug=False)``
===================================================================================

This handles HEAD requests. It gets the response from the **view**, then removes its body. It returns the response with its headers body removed.

**Parameters:**
 - **view** (``func``) - The view function to run.
 - **kwargs** (``dict``) - The kwargs for the view function.
 - **request** (``Request``) - The request to pass to the ``view``.
 - **debug** (``bool``) (optional) - If debug mode it on.
 
**Returns:** ``HTTPResponse``

==============================================================================
``function waffleweb.methodHandler.handleOptions(view, request, debug=False)``
==============================================================================

This handles OPTIONS requests. It adds the "Allow" header with the view's allowed methods. It returns the the response with the "Allow" header included.

**Paramters:**
 - **view** (``func``) - The view function to run.
 - **request** (``Request``) - The request to pass to the ``view``.
 - **debug** (``bool``) - If debug mode is on.

**Returns:** ``HTTPResponse``

====================================================================================
``function waffleweb.methodHandler.handleOther(view, kwargs, request, debug=False)``
====================================================================================

This handles any other methods. All it does is run the view, then returns the response.

**Paramters:**
 - **view** (``func``) - The view function to run.
 - **kwargs** (``bool``) - The kwargs to pass to the ``view``.
 - **request** (``list``) - The request to pass to the ``view``.
 - **debug** (``list``) - If debug mode it on.

**Returns:** ``HTTPResponse``