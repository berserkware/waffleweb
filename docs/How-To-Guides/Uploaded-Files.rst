======================
How-To: Uploaded Files
======================

Uploaded files are key to any image based social media platform. Waffleweb makes receiving and using uploaded files easy. 

File uploads are stored in the ``FILES`` attribute of the ``Request`` object passed into your route functions. The files are stored in ``File`` objects. You can access the data of the file with the ``data`` attribute. You can access the name of the file with the ``name`` attribute.

The data of files are stored in bytes so to save the file you will need to set the mode of ``open()`` to "wb".

.. code-block:: python

	from waffleweb.static import openStatic
	from waffleweb.response import render
	import bleach

	@app.route('/upload', methods=['GET', 'POST'])
	def upload(request):
	    if request.method == 'POST':
	        file = request.FILES.get('file', None)
	        if file is not None:
	            name = bleach.clean(file.name)
	            with openStatic(f'uploads/{name}', 'wb') as f:
	                f.write(file.data)
	    
	    return render(request, 'uploadForm.html')
	    
You should clean the data to prevent data that could break things.

If your are using the built-in test server some of your files may not be fully uploaded. This is becuase of the request size limit. You can get around this by using a WSGI server, See `Deploying Your Project <Deploying-Your-Project.html>`_.

You can access the content type of the file with the ``contentType`` attribute.

The size of the file is stored in the ``size`` attribute.