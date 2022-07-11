====================
How-To: Static Files
====================

All good websites need static files like images, fonts and CSS. In this How-To guide you will be guided through how to access and use static files. You will also be shown how to modify certain things, like changing how Waffleweb looks for static files.

Adding Static Files
...................

You can add static files to your project by creating a directory in your project with your ``STATIC_DIR`` (default is "/static") and putting your static files in there. 

Changing the Static Directory
.............................

To change the directory in which static files are looked for in you can create a file in your project directory called "settings.py". Then in that file add a variable called "STATIC_DIR" with the path for Waffleweb to look for static files in.

``settings.py:``

.. code-block:: python

	STATIC_DIR = 'files/static'

Accessing Static Files
......................

You can access static files from your templates or from your route functons.

Accessing in Routes
-------------------

To access your static files from your route functions you can use the ``openStatic()`` function. ``openStatic()`` takes all the same arguments as ``open()`` except by default it looks under your ``STATIC_DIR`` (default is "/static"). You can change how ``openStatic()`` looks for static files. We will get into that later. ``openStatic()``'s mode by default is "rb" because the ``FileResponse`` takes a binary file.

.. code-block:: python

	from waffleweb.static import openStatic
	from waffleweb.response import FileResponse

	@yourApp.route('/file', methods=['GET'])
	def file(request):
	    with openStatic('file.jpg') as f:
		      return FileResponse(request, f)
		      
Accessing in Templates
----------------------

Whenever a URL ends with a file extension Waffleweb looks for a static file with that path using ``openStatic()``. if ``openStatic()`` returns a file, a ``FileResponse`` is sent, but if it doesn't return a file then it sends a 404 page. By default it looks under your ``STATIC_DIR`` (default is "/static"). You can also access it in the browser this way.

To access "./STATIC_DIR/CSS/index.css" in the browser you can go to "localhost:8000/CSS/index.css".

.. code-block:: html

    <img src="/file.jpg" alt="File">
    
Changing How Waffleweb Looks For Static Files
.............................................

To change how Waffleweb looks for static files you can make your own function to find static. To do this you can create a file called "settings.py". Then in that file you need to add a variable called "DEFUALT_STATIC_FINDER" with the function to find static. By default Waffleweb uses the ``findStatic`` function.

.. code-block:: python

	DEFUALT_STATIC_FINDER = staticFinderFunction

Your static finder function should take all the same arguments as ``open()`` and return what ``open()`` returns. It should return a file in bytes.

The ``DEFUALT_STATIC_FINDER`` is called by ``openStatic()`` with all its arguments. ``openStatic()`` returns what the ``DEFUALT_STATIC_FINDER`` returns.

When a file is accessed from the browser Waffleweb calls function as so:

.. code-block:: python 

	#Accessed URL: "localhost:8000/CSS/file.css"

	DEFUALT_STATIC_FINDER('CSS/file.css', 'rb', -1, None, None, None, True, None)