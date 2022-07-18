===============
How-To: Cookies
===============

Cookies are very useful for a variety of purposes. Some purposes include analytics and tracking logins. Waffleweb makes it easy to set cookies and access cookies.

Accessing Cookies
.................

Sent cookies are stored in the COOKIES attribute of the request. The cookies are stored in a `Cookies <../Reference/cookie.py.html>`_ object. The `Cookies <../Reference/cookie.py.html>`_ object act just like a normal dictionary except it has some special ability used by Waffleweb internally. All the cookies are stored in `Cookie <../Reference/cookie.py.html>`_ Objects. To access the value of the cookies you can use the ``value`` attribute.

.. code-block:: python

	from waffleweb.response import render

	@app.route('/index', methods=['GET'])
	def index(request):
	    cookie = request.COOKIES.get('cookie', None)
	    if cookie is not None:
	        doStuff(cookie.value)
	    
	    return render(request, 'index.html')	
	    
Adding Cookies
..............

You can add cookies to the response with the ``setCookie()`` method. ``setCookie()`` takes 8 arguments: the first two are required but the other 6 are optional. The first two are the name and value of the cookie. The other six are as so:

- **path** (optional) (``str``) - The path of the cookie, defaults to the route of your app.
- **maxAge**  (optional) (``str``) - The maximum age of the cookie.
- **domain** (optional) (``str``) - The domain of the cookie.
- **secure** (optional) (``bool``) - If the cookie is secure.
- **HTTPOnly** (optional) (``bool``) - If the cookie is HTTP Only.
- **sameSite** (optional) (``str``) - If your cookie is first-party of same-site.
 
.. code-block:: python

	from waffleweb.response import render

	@app.route('/index', methods=['GET'])
	def index(request):
	    res = render(request, 'index.html')
	    
	    cookie = request.COOKIES.get('cookie', None)
	    if cookie is not None:
	        doStuff(cookie.value)
	    else:
	        res.setCookie(name='cookie', value='value')
	        
	    return res
	    
Deleting Cookies
................

If you add a cookie to a response and want to delete you can use the ``deleteCookie()`` method. ``deleteCookie()`` takes only one argument: the name of the cookie. If the cookie cannot be found a ``ValueError`` is raised.

.. code-block:: python

	from waffleweb.response import render

	@app.route('/index', methods=['GET'])
	def index(request):
	    res = render(request, 'index.html')
	    
	    res.setCookie(name='cookie', value='value')
	    res.deleteCookie('cookie')
	        
	    return res