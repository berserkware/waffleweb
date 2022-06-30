====================
How-To: Static Files
====================

All good websites need static files like images, fonts and CSS. In this How-To guide you will be guided through how to access static files and using them. You will also be shown how to modify certain things, like changing how Waffleweb looks for static files.

Adding Static Files
...................

You can add static files to your project by creating a directory in your project with your ``STATIC_DIR`` (default is "/static") and putting your static files in there. 

Changing the Static Directory
.............................

To change the directory in which static files are looked for in, you can create a file in your project directory called "settings.py". Then in that file add a variable called "STATIC_DIR" with the path for Waffleweb to look for static files in.

``settings.py:``

.. code-block:: python

	STATIC_DIR = 'files/static'

Accessing Static Files
......................

You can access static files from your templates or from your route functons.

Accessing in Routes
-------------------

To access your static files from your route functions, you can use the ``openStatic()`` function. ``openStatic()`` takes all the same arguments as ``open()`` except by default it looks under your ``STATIC_DIR`` (default is "/static") . You can change how ``openStatic()`` looks for static files, we will get into that later. ``openStatic()``'s mode by default is "rb" because the ``FileResponse`` takes a binary file.

.. code-block:: python

	from waffleweb.static import openStatic
	from waffleweb.response import FileResponse

	@yourApp.route('/file', methods=['GET'])
	def file(request):
	    with openStatic('file.jpg') as f:
		      return FileResponse(request, f)
		      
Accessing in Templates
----------------------

Whenever a URL ends with a file extension, Waffleweb looks for a static files with that path using ``openStatic()``, if it returns a file it a ``FileResponse`` is sent, but if it doesn't return a file then it sends a 404 page. By default it looks under your ``STATIC_DIR`` (default is "/static"). You can also access it in the browser this way.

.. code-block:: html

    <img src="/file.jpg" alt="File">
    
Changing How Waffleweb Looks For Static Files
.............................................

To change how Waffleweb looks for static files you can make your own function to find static. To do this you can create a file called "settings.py". Then in that file you need to add a variable called "DEFUALT_STATIC_FINDER" with the function to find static. By default Waffleweb uses the ``findStatic`` function.

.. code-block:: python

	DEFUALT_STATIC_FINDER = staticFinderFunction

Your static finder function should take all the same arguments as ``open()`` and return what ``open()`` returns. It should return a file in bytes.

The ``DEFUALT_STATIC_FINDER`` is called by ``openStatic()`` with all its arguments. ``openStatic()`` returns what the ``DEFUALT_STATIC_FINDER`` returns.