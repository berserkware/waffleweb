==============================
How-To: Deploying Your Project
==============================

Waffleweb allows you to deploy your application with WSGI. You should not use the server built into Waffleweb, this is because the test server doesn't have good security and it has a request size limitations. In this How-To guide you will be shown how to deploy your project with `Gunicorn <https://gunicorn.org/>`_. 

Installing Gunicorn
-------------------

To install Gunicorn you can use pip.

.. code-block:: bash

	$ pip install gunicorn
	
Getting The WSGI Callable
-------------------------

The WSGI callable is a method of your WaffleProject called "wsgiApplication". Make sure you only put the name of the method. Do not call the method.

.. code-block:: python

	wsgiApp = app.wsgiApplication
	
Connecting The Callable To Gunicorn
-----------------------------------

Connecting the WSGI callable to Gunicorn is easy. Just go to your project directory in the terminal and run this command.

.. code-block:: bash

	$ gunicorn app:wsgiApp
	
In your terminal you should now see something like this:

.. code-block::

	[2022-07-02 17:34:48 +1200] [18669] [INFO] Starting gunicorn 20.1.0
	[2022-07-02 17:34:48 +1200] [18669] [INFO] Listening at: http://127.0.0.1:8000 (18669)
	[2022-07-02 17:34:48 +1200] [18669] [INFO] Using worker: sync
	[2022-07-02 17:34:48 +1200] [18670] [INFO] Booting worker with pid: 18670

If you go to http://127.0.0.1:8000 you should now see your website working.

For more information on Gunicorn you can go to the `Gunicorn Docs <https://docs.gunicorn.org/en/stable/index.html>`_.