"""
valify
~~~~~~

A composable, expressive data validation library for Python.

Basic usage::

    from valify import Schema, StringValidator, IntValidator

    schema = Schema({
        "name": StringValidator(min_length=2),
        "age":  IntValidator(min_value=0, max_value=120),
    })

    result = schema.validate({"name": "Alice", "age": 30})
"""

from __future__ import annotations

from .exceptions import (
    ValifyError, 
    ValidationError, 
    SchemaError,
    RequiredFieldError
)
from .validators import (
    Validator,
    StringValidator,
    IntValidator,
    FloatValidator,
    BoolValidator,
    EmailValidator,
    OptionalValidator,
    ListValidator,
    EnumValidator,
) 

from .schema import Schema

# __all__ defines the public API — what gets exported when someone writes
# `from valify import *`. More importantly, it tells IDEs and documentation
# tools exactly what your library exposes publicly.

__all__ = [
    
    # Exceptions
    "ValifyError",
    "ValidationError",
    "RequiredFieldError",
    "SchemaError",
    
    # Validators
    "Validator",
    "StringValidator",
    "IntValidator",
    "FloatValidator",
    "BoolValidator",
    "EmailValidator",
    "OptionalValidator",
    "ListValidator",
    "EnumValidator",
    
    # Schema
    "Schema",    
]

__version__ = "0.5.0"
__author__ = "Darshan Bamankar"

