==================
Testing  Waffleweb
==================

This page is for how to test waffleweb waffleweb on the backend. If you are contributing to waffleweb, you will probably need to write tests.

=================
Running the Tests
=================

To run the tests all you have to do is download the repository from `here <https://github.com/Berserkware/waffleweb>`_. You can then traverse to folder in the terminal, and run the following command.

.. code-block:: bash

	python3 -m unittest discover -s tests -p '*Test.py'


If the tests are not running, make sure Waffleweb is installed.

=============
Writing Tests
=============

The Waffleweb tests use the unittest library. To learn how to use the unittest library you can go to `this tutorial <https://www.datacamp.com/tutorial/unit-testing-python>`_.

Special Testing Methods
=======================

``WaffleApp`` objects have a special method for sending test requests to the apps without running a server. The method is called ``request``. The ``request`` method takes one argument: a raw bytes request. The request goes through the same process that requests take when going through the server. This means that middleware will also work.

.. code-block:: python

	import unittest

	class TestClass(unittest.TestCase):
	    def test_app(self):
	        app = WaffleApp('testApp')
	        
	        @app.route('/index')
	        def index(request):
	            return HTTPResponse(request, 'index')
	            
	        res = app.request(b'GET /index HTTP/1.1\r\n\r\n')
	        self.assertEqual(res.content, b'index')