=================
How-To: Responses
=================

For your routes to work properly they have to return a response. Waffleweb provides several responses for you to use in your application. There are several types of responses built into Waffleweb such as files, json and html.

Responses
.........

**HTTPResponse**
-----------------

The ``HTTPResponse`` is the most basic of all the responses. It is just a basic response for text. The first argument is the request passed into your routed function. The second argument is the content of the response. The Date and Content-Length headers are automatically added to the response.

.. code-block:: python

	from waffleweb.response import HTTPResponse

	@app.route('/index')
	def index(request):
	    return HTTPResponse(request, 'The index page.')

To change the status of the response you can use the ``status`` argument.

.. code-block:: python

	from waffleweb.response import HTTPResponse

	@app.route('/about')
	def about(request):
	    return HTTPResponse(request, 'The about page.', status=402)
	    
To change the content type of the response you can use the ``contentType`` argument.

.. code-block:: python

	from waffleweb.response import HTTPResponse

	@app.route('/text')
	def text(request):
	    return HTTPResponse(request, 'Some text', contentType='text/plain')
	    
You can add headers with the ``headers`` attribute. The headers are stored in a `MultiValueOneKeyDict <../Reference/datatypes.py.html>`_. For more advanced usage go to there.
	    
.. code-block:: python

	from waffleweb.response import HTTPResponse
	    
	@app.route('/index')
	def index(request):
	    res = HTTPResponse(request, 'The index page.')
	    res.headers['headerName'] = 'value'
	    res.headers['otherHeader'] = ['value1', 'value2']
	    return res
	    
To add cookies you can use the ``setCookie()`` method. The path of the cookies are automatically set to the path of your route. For more information you can go to `Cookies <Cookies.html>`_. You can delete a cookie from a response just as easily with the ``deleteCookie()`` method. If the cookie cannot be found it will raise a ``ValueError``.

.. code-block:: python

	from waffleweb.response import HTTPResponse
	    
	@app.route('/cookie')
	def cooke(request):
	    res = HTTPResponse(request, 'The index page.')
	    res.setCookie('cookieName', 'value')
	    res.deleteCookie('cookieName')
	    return res
	    
**JSONResponse**
----------------

``JSONResponse`` is for JSON responses. It can be particularly useful for APIs. It inherits from the HTTPResponse class. The first argument is the request passed into your routed function. The second argument is a JSON serializable object.

.. code-block:: python

	from waffleweb.response import JSONResponse

	@app.route('/data')
	def data(request):
	    return JSONResponse(request, {'number': 123})
	    
As it inherites from the ``HTTPResponse`` class you can do most of the same things with it as the ``HTTPResponse``, such as adding headers and cookies.

**FileResponse**
----------------

``FileResponse`` is a response for files. It inherits from the HTTPResponse class. The first argument is the request passed into your routed function. The second argument is a bytes file object. The mimetype of the file is guessed if you don't provide the ``mimeType`` argument.

.. code-block:: python

	from waffleweb.response import FileResponse
	from waffleweb.static import openStatic
	
	@app.route('/file')
	def file(request):
	     with openStatic('testFile.jpeg') as f:
	         return FileResponse(request, f)
	         
``openStatic()`` looks in your ``STATIC_DIR`` directory for files and its mode is set to 'rb'. To learn more about static functions you can go to `Static Files <Static-Files.html>`_. If you want to use the normal ``open()`` function, just set the ``mode`` argument to 'rb'

**render()**
------------

``render()`` is a response for templates. The first argument is the request passed into your routed function. The second argument is the path to the template. It looks under your ``TEMPLATE_DIR`` for the templates. The third optional argument is the variables for the templates. ``render()`` uses Jinja2 for templating by default.

.. code-block:: python

	from waffleweb.response import render
	
	@app.route('/template')
	def template(request):
	    return render(request, 'template.html', {'var1': '1234'})
	    
To learn more about templating you can go to `Templating <Templating.html>`_

Redirects
.........

**HTTPResponseRedirect**
------------------------

``HTTPResponseRedirect`` is a redirect. Its only argument is the location to redirect to.

.. code-block:: python

	from waffleweb.response import HTTPResponseRedirect
	
	@app.route('/redirect')
	def redirect(request):
	    return HTTPResponseRedirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
	    
**HTTPResponsePermenentRedirect**
---------------------------------

``HTTPResponsePermenentRedirect`` is a permanent redirect. Its only argument is the location to redirect to.

.. code-block:: python

	from waffleweb.response import HTTPResponsePermenentRedirect
	
	@app.route('/permanentRedirect')
	def permanentRedirect(request):
	    return HTTPResponsePermenentRedirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
	    
**redirect()**
--------------

A shortcut for redirects. It takes two arguments: the place to redirect to and whether or not it is a permanent redirect or not.

.. code-block:: python

	from waffleweb.response import redirect
	
	@app.route('/redirect')
	def redirect(request):
	    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ', permanent=True)