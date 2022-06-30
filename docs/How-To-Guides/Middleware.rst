==================
How-To: Middleware
==================

Middleware is code that modifies the request before going into your code and the response after coming out of your route function. Waffleweb allows you to add middleware to your apps and project easily.

Adding Middleware
..................

Project Wide Middleware
-----------------------

To add middleware to your entire project you can add the ``middleware`` argument to your ``WaffleProject``. The ``middleware`` argument is a list of your middleware. All the middleware are strings with the module and middleware class. Example: 'testModule.Middleware' or 'middleware.testModule.Middleware'.

.. code-block:: python

	from waffleweb import WaffleProject

	apps = [
	    #Your apps
	]

	middleware = [
	    'middleware.addCookieMiddleware.AddCookie'
	]

	proj = WaffleProject(apps=apps, middleware=middleware)
	
App Specific Middleware
-----------------------

To add app-specific middleware is much the same as adding middleware to your project. All you need to do is add the ``middleware`` argument to your ``WaffleApp``. The middleware is again a list formatted the same way as the project-wide middleware.

.. code-block:: python

	from waffleweb import WaffleApp

	middleware = [
	    'middleware.addCookieMiddleware.AddCookie'
	]

	app = WaffleApp('app', middleware=middleware)
	
Creating Middleware
....................

Creating middleware for Waffleweb is easy. The middleware is class with one or two methods named "after" and "before". The "after" method should take a ``Request`` object and return a ``Request`` object. The "before" method should take a response and return a response.

.. code-block:: python

	class ExampleMiddleware:
	    def before(request):
	        request.COOKIES['cookie'] = 'value'
	        return request
	    
	    def after(response):
	        response.headers['header'] = 'value'
	        return response
	        
Please note that you don't need both methods, you only need one of two methods.