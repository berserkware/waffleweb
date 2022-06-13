==========
project.py
==========

Project object
..............
``class waffleweb.WafflewebProject(apps, middleware=[])``
.........................................................

The WafflewebProject object is where you can access the wsgi app and a test server. It is also a central point for your project.

**Parameters:**
 - **apps** (``list[str]``) - A list of all your apps. All the apps are strings with the module and the WaffleApp name. Example: 'testModule.yourApp' or 'apps.testModule.yourApp'.
 - **middleware** (optional) (``list[str]``) - A list of your middleware. All the middleware are strings with the module and middleware class. Example: 'testModule.Middleware' or 'middleware.testModule.Middleware'.

------------------
``loadApps(apps)``
------------------

Loads all the apps into a list.

**Parameters:**
 - **apps** (``list[str]``) - A list of apps. All the apps are strings with the module and the WaffleApp name. Example: 'testModule.yourApp' or 'apps.testModule.yourApp'.

**Returns:** ``list``

-------------------------------------------------
``run(host='127.0.0.1', port=8000, debug=False)``
-------------------------------------------------

Runs a test server. Shouldn't be used in production.

**Parameters:**
 - **host** (optional) (``str``) - The host of your website.
 - **port** (optional) (``int``) - The port of your website.
 - **debug** (optional) (``bool``) - If your server is in debug mode.

-------------------------------------------
``wsgiApplication(environ, startResponse)``
-------------------------------------------

A WSGI application. As outlined in `PEP 3333 <https://peps.python.org/pep-3333/>`_.

**Parameters:**
 - **environ** (``dict``) - For your wsgi server gateway. As outlined in `PEP 3333 <https://peps.python.org/pep-3333/>`_.
 
 - **startResponse** (``func``) - For your wsgi server gateway. As outlined in `PEP 3333 <https://peps.python.org/pep-3333/>`_.