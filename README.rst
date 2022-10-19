=========
Waffleweb
=========

.. image:: https://img.shields.io/github/license/berserkware/waffleweb
   :alt: github

.. image:: https://readthedocs.org/projects/waffleweb/badge/?version=latest
    :target: https://waffleweb.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/waffleweb
   :alt: PyPI

Waffleweb is a WSGI Python web framework for making web applications easily. Waffleweb is highly customizable and doesn't force any project layout.

------------
Installation
------------ 
You can install Waffleweb with `pip <https://pip.pypa.io/en/stable/>`_.

.. code-block:: bash

	pip install waffleweb

----------------
A Simple Example
----------------

.. code-block:: python

	from waffleweb import app
	from waffleweb.response import HTTPResponse, render
	
	@app.route('/index')
	def index(request):
	    return HTTPResponse(request, 'index')
	    
	@app.route('/article/<id:int>/<name:str>')
	def articleView(request, id, name):
	    return render(request, 'articleView.html', context=findArticle(id, name))
	    
	app.run()

-------------
Documentation
-------------
You can find the documentation at https://waffleweb.readthedocs.io.

------------
Contributing
------------
To contribute to Waffleweb all you need to do fork the repo and change what you thing needs to be changed. You can then submit a pull request for review.

-----
Links
-----
- Documentation- https://waffleweb.readthedocs.io
- Changes - https://berserkware.github.io/waffleweb/changes
- Source Code - https://github.com/Berserkware/waffleweb
- Website - https://berserkware.github.io/waffleweb
- Discord - https://discord.gg/U6HjwhkcGr