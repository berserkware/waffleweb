=============
How-To: Forms
=============

For users to submit data to your server you can use forms. Forms are vital for account systems and social media sites. In this How-To guide you will learn how to make forms and access the data in your routes.

Basic forms
...........

The form we are going to make is to get data and save it to a json file. To create a basic form we first need to route a function. We also need to make a html page for the form.

``app.py:``

.. code-block:: python

	from waffleweb.response import render

	@yourApp.route('/form')
	def form(request):
	    return render(request, 'form.html')
		  
``form.html:``

.. code-block:: html

	<h1>Form:</h1>
	<form method="post">
	    <label for="username">Username:</label>
	    <input type="text" name="username"><br>
	    <label for="favThing">Favourite Thing:</label>
	    <input type="text" name="favThing"><br>
	    <button type="submit">Submit</button>
	</form>
	
Now we need to add logic to our route. We also need to create a folder called 'static' with a file called 'data.json'. For the the logic to work we need add some boilerplate data to the file.

``data.json:``

.. code-block:: json

	{"entries": []}

``app.py:``

.. code-block:: python

	import json
	import bleach
	from waffleweb.static import openStatic
	from waffleweb.response import render

	@yourApp.route('/form', methods=['GET', 'POST'])
	def form(request):
	    if request.method == 'POST':
	        name = bleach.clean(request.POST.get('username', 'N/A'))
	        favThing = bleach.clean(request.POST.get('favThing', 'N/A'))
		      
	        with openStatic('data.json', 'r') as f:
	            data = json.loads(f.read())
		          
	        with openStatic('data.json', 'w') as f:
	            entry = {'username': name, 'favThing': favThing}
	            data['entries'].append(entry)
	            f.write(json.dumps(data))
		          
	    return render(request, 'form.html')

All the data from the form is stored in the ``POST`` attribute. The get method is used for retrieving data in case the client doesn't send the correct data. The `bleach <https://bleach.readthedocs.io/en/latest/>`_ library is used to clean the data in this example.

File Forms
..........

If your are making a social media you will probably need to accept file uploads. The uploaded files of the request are stored in the ``FILES`` attribute. This form will take a file and the server will save it. You need to set the ``enctype`` of the form to "multipart/form-data", so that the data of the file goes through.

``upload.html:``

.. code-block:: html

	<h1>Upload:</h1>
	<form method="post" enctype="multipart/form-data">
	    <label for="file">File:</label><br>
	    <input type="file" name="file"><br>
	    <button type="submit">Submit</button>
	</form>
  
``app.py:``

.. code-block:: python

	from waffleweb.static import openStatic
	from waffleweb.response import render

	@yourApp.route('/upload', methods=['GET', 'POST'])
	def upload(request):
	    if request.method == 'POST':
	        file = request.FILES['file']
	        with openStatic(f'{file.name}/', 'wb') as f:
	            f.write(file.data)
	    return render(request, 'upload.html')
		  
All the files are stored in ``File`` objects. The data is stored in bytes in the ``data`` attribute. Because of this, to save the file you have to set the mode of ``openStatic()`` to 'wb'. The name of the file is stored in the ``name`` attribute.

If your want to learn more about file uploads you can go to the `Uploaded Files <Uploaded-Files.rst>`_ How-To guide.