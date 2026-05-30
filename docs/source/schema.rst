Schema
======

The ``Schema`` class validates a dictionary of data against
a set of validators — one validator per field.

Basic usage
-----------

.. code-block:: python

   from valify import Schema, StringValidator, IntValidator

   schema = Schema({
       "name": StringValidator(min_length=2),
       "age":  IntValidator(min_value=0),
   })

   result = schema.validate({"name": "Alice", "age": 30})

Strict mode
-----------

By default extra fields in the data are silently ignored.
In strict mode they raise ``ValidationError``:

.. code-block:: python

   schema = Schema(
       {"name": StringValidator()},
       strict=True,
   )

   # Raises ValidationError — 'extra' is not in the schema
   schema.validate({"name": "Alice", "extra": "field"})

Nested schemas
--------------

``Schema`` inherits from ``Validator``, so it can be used
as a field value inside another schema:

.. code-block:: python

   address_schema = Schema({
       "city": StringValidator(),
       "pin":  StringValidator(min_length=6),
   })

   user_schema = Schema({
       "name":    StringValidator(),
       "address": address_schema,
   })

API reference
-------------

.. autoclass:: valify.schema.Schema
   :members:
   :show-inheritance: