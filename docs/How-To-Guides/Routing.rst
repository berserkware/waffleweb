===============
How-To: Routing
===============

Routing enables you to bind a function to an URL. In this How-To guide you will lea

Basics of routing
.................

To route a view you need to use the ``route()`` decorator.

.. code-block:: python

	@yourApp.route(path='/index', name='indexPage', methods=['GET'])
	def index(request):
	    return HTTPResponse(request, 'Index page.')
	    
The path parameter is the URI of the route