"""
valify.exceptions
~~~~~~~~~~~~~~~~~

Custom exception hierarchy for the valify library.
"""

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
    
    def __init__(self, message, *, field = None, value = None):
        
        self.message = message
        self.field = field
        self.value = value
        
        full_message = f"[{field}] {message}" if field else message
        super().__init__(full_message)

class RequiredFieldError(ValidationError):
    """ Raised when a required field is missing from validation data. """
    
    def __init__(self, field):
        super().__init__(
            message="Required field is missing",
            field=field,
            value=None,
        )

class SchemaError(ValifyError):
    """ Raised when the schema definition itself is inavlid.  """
    
    def __init__(self, message):
        self.message = message
        super().__init__(message)
    