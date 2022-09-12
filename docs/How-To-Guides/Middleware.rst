==================
How-To: Middleware
==================

Middleware is code that modifies the request before going into your code, and the response after coming out of your route function. Waffleweb allows you to add middleware to your app easily.

Adding Middleware
..................

To add middleware you can use the ``middleware`` attribute of the ``app`` instance. All the middleware are classes.

.. code-block:: python

	from waffleweb import app
    from yourMiddleware import middleware

	app.middleware.append(middleware)
	
The order in which the middleware gets called is the first middleware you add is the first run.
	
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