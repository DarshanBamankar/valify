Quick Start
===========

Basic validation
----------------

.. code-block:: python

   from valify import Schema, StringValidator, IntValidator, EmailValidator

   schema = Schema({
       "name":  StringValidator(min_length=2, max_length=50),
       "age":   IntValidator(min_value=0, max_value=120),
       "email": EmailValidator(),
   })

   result = schema.validate({
       "name":  "Alice",
       "age":   30,
       "email": "alice@example.com",
   })
   print(result)
   # {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}

Handling errors
---------------

valify reports ALL errors at once, not just the first one:

.. code-block:: python

   from valify.exceptions import ValidationError

   try:
       schema.validate({
           "name":  "A",
           "age":   -5,
           "email": "not-an-email",
       })
   except ValidationError as e:
       print(e)
   # Validation failed:
   #   name: Must be at least 2 characters long.
   #   age: Must be at least 0.
   #   email: 'not-an-email' is not a valid email address.

Optional fields
---------------

.. code-block:: python

   from valify import Schema, StringValidator, OptionalValidator

   schema = Schema({
       "name": StringValidator(min_length=2),
       "bio":  OptionalValidator(StringValidator(), default=""),
   })

   # bio is missing — returns default value instead of erroring
   result = schema.validate({"name": "Alice"})
   print(result)
   # {'name': 'Alice', 'bio': ''}

Nested schemas
--------------

.. code-block:: python

   from valify import Schema, StringValidator, IntValidator

   address_schema = Schema({
       "street": StringValidator(min_length=2),
       "city":   StringValidator(min_length=2),
       "pin":    StringValidator(min_length=6, max_length=6),
   })

   user_schema = Schema({
       "name":    StringValidator(min_length=2),
       "age":     IntValidator(min_value=0),
       "address": address_schema,
   })

   user_schema.validate({
       "name": "Alice",
       "age":  30,
       "address": {
           "street": "MG Road",
           "city":   "Pune",
           "pin":    "411001",
       }
   })