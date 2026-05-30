Exceptions
==========

valify defines its own exception hierarchy so you can catch
errors precisely.

Hierarchy
---------

.. code-block:: text

   Exception
   └── ValifyError
       ├── ValidationError
       │   └── RequiredFieldError
       └── SchemaError

Usage
-----

Catch a specific error:

.. code-block:: python

   from valify.exceptions import ValidationError

   try:
       schema.validate(data)
   except ValidationError as e:
       print(e.field)    # which field failed
       print(e.value)    # what value was rejected
       print(e.message)  # human readable message

Catch everything valify raises:

.. code-block:: python

   from valify.exceptions import ValifyError

   try:
       schema.validate(data)
   except ValifyError as e:
       print(f"valify error: {e}")

API reference
-------------

.. autoclass:: valify.exceptions.ValifyError
   :members:
   :show-inheritance:

.. autoclass:: valify.exceptions.ValidationError
   :members:
   :show-inheritance:

.. autoclass:: valify.exceptions.RequiredFieldError
   :members:
   :show-inheritance:

.. autoclass:: valify.exceptions.SchemaError
   :members:
   :show-inheritance: