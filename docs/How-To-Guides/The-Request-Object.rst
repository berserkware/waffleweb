==========================
How-To: The Request Object
==========================

The ``Request`` object stores all the data of the request. It stores stuff like POST data, file uploads, cookies and headers. The ``Request`` object is passed into your view functions as the first argument. If you are looking for the API reference of the Request object you can go to the `request.py </Reference/request.py.rst>`_ page.

To get the method of request you can use the ``method`` attribute.

.. code-block:: python

	from waffleweb.response import render

	@yourApp.route('/upload', methods=['GET', 'POST'])
	def upload(request):
	    if request.method == 'POST':
	        return doUploadStuff(request)
	    else:
	        return render(request, 'form.html')
	
Accessing headers
.................

The headers of the request is stored in a ``dict`` in the ``META`` attribute. It is recommended to use ``get()`` to get the POST data as the client might not the send the expected headers.

.. code-block:: python 

	from waffleweb.response import render

	@yourApp.route('/page', methods=['GET'])
	def page(request):
	    userAgent = request.META.get('USER_AGENT', None)
	    if userAgent == 'agent':
	        return render(request, 'page1.html')
	    else:
	        return render(request, 'page2.html')

	
Accessing POST data
...................

The POST data of the request is stored in a ``dict`` in the ``POST`` attribute. It is recommended to use ``get()`` to get the POST data as the client might not the send the expected POST data.

.. code-block:: python

	from waffleweb.response import render

	@yourApp.route('/form', methods=['GET', 'POST'])
	def form(request):
	    if request.method == 'POST':
	        name = request.POST.get('name', 'john_doe')
	        doStuff(name)
	    return render(request, 'form.html')
	    
Accessing file uploads
......................

The file uploads of the request is stored in a ``dict`` in the ``FILES`` attribute. All the files are ``File`` objects. The content of the file is stored in the ``data`` attribute of the file and the name is stored in the ``name`` attribute.

.. code-block:: python

	from waffleweb.response import render

	@yourApp.route('/upload', methods=['GET', 'POST'])
	def form(request):
	    if request.method == 'POST':
	        file = request.FILES.get('file', None)
	        if file is not None:
	            with open(f'files/{file.name}', 'x') as f:
	                f.write(file.data)
	                
	    return render(request, 'upload.html')
	    
In a real life situation you should make sure the content or name is clean.

For more information you can go to `Uploaded Files <Uploaded-Files.rst>`_. 

Accessing URL parameters
........................

URL parameters are the '?paramName=value' at the end of the URL. URL parameters are useful for when you want to send data in a GET request. URL parameters are stored in a ``dict`` in the ``URL_PARAMS`` attribute. Again it is recommended to use ``get()`` to get the parameters data as the client might not the send the correct parameters.

.. code-block:: python

	from waffleweb.response import render

	@yourApp.route('/search', methods=['GET'])
	def search(request):
	    term = request.URL_PARAMS.get('term', None)
	    if term is None:
	        return render(request, 'searchPage.html')
	    
	    results = getResults(term)
	    return render(request, 'searchResults.html', {'results': results})
	    
As this is just an example it does not clean the data, but in a real life scenario you should clean the data.

Accessing cookies
.................

Cookies are very useful for many reasons, such as identifying users. Cookies are stored in a ``dict`` as ``Cookie`` objects in the ``COOKIES`` attribute. Once again it is recommended to use ``get()`` to get the parameters data, as the client might not the send the correct cookies. You can access the value of the cookie with the ``value`` attribute.

.. code-block:: python

	from waffleweb.response import render

	@yourApp.route('/enter', methods=['GET'])
	def enter(request):
	    if 'name' in request.COOKIES.keys():
	        if request.COOKIES['name'].value == 'john':
	            return render(request, 'secret.html')
	        else:
	            return render(request, 'user.html', {'name': request.COOKIES['name'].value})
	    else:
	        return render(request, 'enter.html')
	   	    
Accessing other data
....................

To access the raw request you can use the ``rawRequest`` attribute.

To access the body of the request you can use the ``body`` attribute.