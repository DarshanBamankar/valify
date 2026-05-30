Validators
==========

All validators accept a value via their ``validate()`` method.
On success they return the validated (possibly coerced) value.
On failure they raise :class:`~valify.exceptions.ValidationError`.

StringValidator
---------------

.. autoclass:: valify.validators.StringValidator
   :members:
   :show-inheritance:

IntValidator
------------

.. autoclass:: valify.validators.IntValidator
   :members:
   :show-inheritance:

FloatValidator
--------------

.. autoclass:: valify.validators.FloatValidator
   :members:
   :show-inheritance:

BoolValidator
-------------

.. autoclass:: valify.validators.BoolValidator
   :members:
   :show-inheritance:

EmailValidator
--------------

.. autoclass:: valify.validators.EmailValidator
   :members:
   :show-inheritance:

OptionalValidator
-----------------

.. autoclass:: valify.validators.OptionalValidator
   :members:
   :show-inheritance:

ListValidator
-------------

.. autoclass:: valify.validators.ListValidator
   :members:
   :show-inheritance:

EnumValidator
-------------

.. autoclass:: valify.validators.EnumValidator
   :members:
   :show-inheritance: