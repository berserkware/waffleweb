===========
template.py
===========

==================================================================
``function waffleweb.template.getRelativeUrl(viewName, **kwargs)``
==================================================================

Gets the URL of the view from the viewName. The kwargs are the URL variables. It uses the views from ``waffleweb.currentWorkingApp``.

**Parameters:**
 - **viewName** (``str``) - The name of the view.
 - ****kwargs** - The URL variables.
 
=====================================================
``function waffleweb.template.getEnvironmentFile()``
=====================================================

Get the environment for Jinja2. It gets a environment with ``FileSystemLoader`` with the searchpath being ``TEMPLATE_DIR`` from the settings.py file, defaults to 'templates/'.

**Returns:** ``Environment``

====================================================================
``function waffleweb.template.renderTemplate(filePath, context={})``
====================================================================

Renders a template, returns the rendered template.

**Parameters:**
 - **filePath** (``str``) - The path to the template.
 - **context** (``dict``) - The variables for the template.
 
**Returns:** ``str``