=========
static.py
=========

==============================================
``function waffleweb.static.findStatic(path)``
==============================================
This function takes a file name or path, and adds the your ``STATIC_DIR`` or the defualt static path to the start of it. This is to separate the static finder from the static opener so you can provide your own static finder.

**Parameters:**
 - **path** (``str``) - The path to find the static file path from.

**Returns:** A file object

============================================================================================================================================
``function waffleweb.static.openStatic(file, mode='rb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)``
============================================================================================================================================

Opens a static file. takes all the same arguments as ``open()``. It's basically just open, but it puts the ``file`` through ``findStatic`` or your static finder function.

**Returns:** a file object

=======================================================================
``function waffleweb.static.getStaticFileResponse(request, root, ext)``
=======================================================================

Finds a static file and puts it into a ``FileResponse``. If cannot find file, it raises HTTP404.

**Parameters:**
 - **request** (``Request``) - The request for the response.
 - **root** (``str``) - The path to the file.
 - **ext** (``str``) - The file extension.
 
**Returns:** ``FileResponse``