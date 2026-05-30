valify
======

A composable, expressive data validation library for Python.

.. code-block:: python

   from valify import Schema, StringValidator, IntValidator

   schema = Schema({
       "name": StringValidator(min_length=2),
       "age":  IntValidator(min_value=0, max_value=120),
   })

   result = schema.validate({"name": "Alice", "age": 30})

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   validators
   schema
   exceptions