============
datatypes.py
============

============================================================================
``class waffleweb.datatypes.MultiValueOneKeyDict(data={}, *args, **kwargs)``
============================================================================
Inherits from ``dict``.

This is a dictionary where one key can have multiple values.

**Parameters:**
 - **data** (optional) (``dict``) - A normal dictionary for initial data, to add multiple values, put them in a list.
 
 .. code-block:: python
 	
 	{'data1': ['value1', 'value2'], 'data2': 'value'}
 	
------
Usage:
------
 	
**Getting:**

Getting a item from a key with only one value:

.. code-block:: python
 	
 	>>> dic = MultiValueOneKeyDict({'data': 'value'})
 	>>> dic['data']
 	'value'

Getting a time from a key with multiple values:

.. code-block:: python
 
	>>> dic = MultiValueOneKeyDict({'data': ['value1', 'value2']})
	>>> dic['data', 1]
	'value2'

Getting all the values of a key:

.. code-block:: python
 
	>>> dic = MultiValueOneKeyDict({'data': ['value1', 'value2']})
	>>> dic['data']
	['value1', 'value2']

**Setting:**

Setting a value to a new key:

.. code-block:: python

	>>> dic = MultiValueOneKeyDict()
	>>> dic['data'] = 'value'
	>>> dic
	{'data': ['value']}
	
Setting multiple values to a new key:

.. code-block:: python
	
	>>> dic = MultiValueOneKeyDict()
	>>> dic['data'] = ['value1', 'value2']
	>>> dic
	{'data': ['value1', 'value2']}
	
Adding a value to an existing key:

.. code-block:: python

	>>> dic = MultiValueOneKeyDict({'data': 'value1'})
	>>> dic['data'] = 'value2'
	>>> dic
	{'data': ['value1', 'value2']}
	
Adding multiple values to an existing key:

.. code-block:: python

	>>> dic = MultiValueOneKeyDict({'data': 'value1'})
	>>> dic['data'] = ['value2', 'value3']
	>>> dic
	{'data': ['value1', 'value2', 'value3']}
	
Changing specific value:

.. code-block:: python

	>>> dic = MultiValueOneKeyDict({'data': ['value1', 'value2']})
	>>> dic['data', 1] = 'newValue'
	>>> dic
	{'data': ['value1', 'newValue']}
	
Overwriting a key:

.. code-block:: python

	>>> dic = MultiValueOneKeyDict({'data': ['value1', 'value2']})
	>>> dic['data', None] = 'newValue'
	>>> dic
	{'data': ['newValue']}
	
**Deleting:**

Deleting a key and all it's values:

.. code-block:: python

	>>> dic = MultiValueOneKeyDict({'data': ['value1', 'value2']})
	>>> del dic['data']
	>>> dic
	{}
	
Deleting a specific value from a key:

.. code-block:: python

	>>> dic = MultiValueOneKeyDict({'data': ['value1', 'value2']})
	>>> del dic['data', 1]
	>>> dic
	{'data': ['value1']}

------------------------------------------
``get(keyname, index=None, default=None)``
------------------------------------------

Return the value of the item with the specified key. If your key has more than one value you will need to provide a index, otherwise it will return all the items. Returns the item.

**Parameters:**
 - **keyname** (``str``) - The key name.
 - **index** (``int``) - The index of the value.
 - **default** (``any``) - If your key cannot be find then return this.
 
**Returns:** ``str`` or ``list``
 
-----------------------------------------------
``setdefault(keyname, index=None, value=None)``
-----------------------------------------------

Return the value of the item with the specified key. If your key has more than one value you will need to provide a index. If the key doesn't exist, set it to the specified value. To overwrite all the items set the index to ``None``. Returns the value of the item.

**Parameters:**
 - **keyname** (``str``) - The key name.
 - **index** (``int``) - If your key has more than one value then you will need to provide the index of the value.
 - **value** (``str``) - Value to set if key doesn't exist.
 
**Returns:** ``str`` or ``list``
 
------------------------------------------
``pop(keyname, index=None, default=None)``
------------------------------------------

Deletes the value at the specified key. If your key has more than one value you can provide an index to specify a value. If your key has more than one value and you don't provide a value it will delete all the values. Returns the deleted value.

**Parameters:**
 - **keyname** (``str``) - The key name.
 - **index** (``int``) - The index of the value.
 - **default** (``any``) - If your key cannot be find then return this.
 
**Returns:** ``str`` or ``list``

----------
``keys()``
----------

Returns all the keys of the dictionary.

**Returns:** ``dict_keys``

-----------
``items()``
-----------

Returns all the items of the dictionary.

**Returns:** ``dict_items``

----------
``copy()``
----------

Returns a copy of the dictionary.

**Returns:** ``dict``
