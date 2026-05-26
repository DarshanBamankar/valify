"""
valify.exceptions
~~~~~~~~~~~~~~~~~

Custom exception hierarchy for the valify library.
"""

from __future__ import annotations
from typing import Any

class ValifyError(Exception):
    """ Base class for all valify exceptions  """
    
class ValidationError(ValifyError):
    """
    Raised when a value fails a validation rule.
    
    Attributes
    ----------
    message : str
        Human-readable description of what failed.
    field : str
        The field name that failed. None if used outside a schema.
    value : object
        The actual value that was rejected.
    """
    
    def __init__(
        self, 
        message: str,
        *, 
        field: str | None = None, 
        value: Any = None
        ) -> None:
        
        self.message: str = message
        self.field: str | None = field
        self.value: Any = value
        
        full_message = f"[{field}] {message}" if field else message
        super().__init__(full_message)

class RequiredFieldError(ValidationError):
    """ Raised when a required field is missing from validation data. """
    
    def __init__(self, field: str) -> None:
        super().__init__(
            message="Required field is missing",
            field =field,
            value=None,
        )

class SchemaError(ValifyError):
    """ Raised when the schema definition itself is inavlid.  """
    
    def __init__(self, message: str) -> None:
        self.message: str = message
        super().__init__(message)
    