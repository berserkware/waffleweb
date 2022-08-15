===========
settings.py
===========

==================================================================
``function waffleweb.settings.getFromSettings(var, default=None)``
==================================================================

Gets a variable from the user's settings.py file. If it cannot find the variable, it returns the ``default`` argument.

**Parameters:**
 - **var** (``str``) - The variable to try to get.
 - **default** (``any``) - The default to return if the variable cannot be found.