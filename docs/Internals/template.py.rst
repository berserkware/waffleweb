===========
template.py
===========

=================================================================
``function waffleweb.template.getRelativeUrl(viewStr, **kwargs)``
=================================================================

Gets the URL of view from the viewStr. A viewStr is `appname:viewname`. The kwargs are the URL variables.

**Parameters:**
 - **viewStr** (``str``) - A string of the app and route of the desired view, Example: `appname:viewname`.
 - ****kwargs** - The URL variables.
 
=====================================================
``function waffleweb.template._getEnvironmentFile()``
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

=============================================================================================
``function waffleweb.template.renderErrorPage(mainMessage, subMessage=None, traceback=None)``
=============================================================================================

Renders an error page for debug mode.

**Parameters:**
 - **mainMessage** (``str``) - The main heading for the error page.
 - **subMessage** (optional) (``str``) - The subheading for the error page.
 - **traceback** (optional) (``str``) - The traceback to the error.
 
**Returns:** ``str``