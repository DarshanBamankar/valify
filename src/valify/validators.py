
"""
valify.validators
~~~~~~~~~~~~~~~~~

Built-in validators for common Python types and patterns.

Each validator is a class that accepts configuration on instantiation
and exposes a single `validate(value)` method that either returns the
(possibly coerced) value or raises ValidationError.
"""

from __future__ import annotations

from typing import Any

import re

from .exceptions import ValidationError


class Validator:
    """Base class for all valify validators.

    All built-in and custom validators inherit from this class.
    Subclasses must implement the `validate` method.

    Example
    -------
    Creating a custom validator::

        class PositiveInt(Validator):
            def validate(self, value: object) -> object:
                if not isinstance(value, int) or value <= 0:
                    raise ValidationError(
                        "Value must be a positive integer.",
                        value=value,
                    )
                return value
    """
    
    def validate(self, value: Any) -> Any:
        """
        Parameters
        ----------
        value : Any
            The value to validate.

        Returns
        -------
        Any
            The validated (and possibly coerced) value.

        Raises
        ------
        ValidationError
            If the value fails validation.
        """
        raise NotImplementedError(
            f"{type(self).__name__} must implement validate()"
        )
        
    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
    
class StringValidator(Validator):
    """Validates that a value is a string, with optional length constraints.

    Parameters
    ----------
    min_length : int or None
        Minimum allowed length. None means no minimum.
    max_length : int or None
        Maximum allowed length. None means no maximum.
    strip : bool
        If True, strip leading/trailing whitespace before validating.
        Defaults to True.

    Example
    -------
        v = StringValidator(min_length=2, max_length=50)
        v.validate("Alice")   # returns "Alice"
        v.validate("A")       # raises ValidationError
    """
    
    def __init__(
        self,
        *, 
        min_length: int | None = None,
        max_length: int | None = None,
        strip: bool = True
        ) -> None:
        
        self.min_length: int | None = min_length
        self.max_length: int | None = max_length
        self.strip: bool = strip
        
    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
                raise ValidationError(
                    f"Expected a string, got {type(value).__name__}",
                    value=value
                )
        if self.strip:
            value = value.strip()
            
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(
                f"Must be at least {self.min_length} characters long.",
                value=value,
            )
        
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(
                f"Must be at most {self.max_length} characters long.",
                value=value,
            )
        
        return value
    
    def __repr__(self) -> str:
        return (
            f"StringValidator("
            f"min_length={self.min_length!r}, "
            f"max_length={self.max_length!r}, "
            f"strip={self.strip!r})"
        )

class IntValidator(Validator):
    """Validates that a value is an integer, with optional range constraints.

    Parameters
    ----------
    min_value : int or None
        Minimum allowed value. None means no minimum.
    max_value : int or None
        Maximum allowed value. None means no maximum.
    coerce : bool
        If True, attempt to convert strings to int before validating.
        Defaults to False.

    Example
    -------
        v = IntValidator(min_value=0, max_value=120)
        v.validate(25)    # returns 25
        v.validate(-1)    # raises ValidationError
    """
    
    def __init__(
        self, 
        *,
        min_value: int | None = None,
        max_value: int | None = None,
        coerce: bool = False
        ) -> None:
        
        self.min_value: int | None = min_value
        self.max_value: int | None = max_value
        self.coerce: bool = coerce
    
    def validate(self, value: Any) -> int:
        if self.coerce and not isinstance(value,int):
            try:
                value = int(value)
            except(ValueError, TypeError):
                raise ValidationError(
                    f"Could not convert {value!r} to int",
                    value=value
                )
        if not isinstance(value, int) or isinstance(value,bool):
            raise ValidationError(
                f"Expected an integer, got {type(value).__name__}.",
                value=value
            )
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(
                f"Must be at least {self.min_value}.",
                value=value,
            )

        if self.max_value is not None and value > self.max_value:
            raise ValidationError(
                f"Must be at most {self.max_value}.",
                value=value,
            )
        return value
    
    def __repr__(self) -> str:
        return (
            f"IntValidator("
            f"min_value={self.min_value!r}, "
            f"max_value={self.max_value!r}, "
            f"coerce={self.coerce!r})"
        )

class FloatValidator(Validator):
    """ Validates that a value is float, with optional range values. 
    
    Parameters
    ----------
    min_value : float or None
        Minimum allowed value. None means no minimum.
    max_value : float or None
        Maximum allowed value. None means no maximum.
    coerce : bool
        If True, attempt to convert strings and ints to float.
        Defaults to False.

    Example
    -------
        v = FloatValidator(min_value=0.0, max_value=1.0)
        v.validate(0.5)   # returns 0.5
        v.validate(1.5)   # raises ValidationError
    """
    
    def __init__(
        self,
        *,
        min_value: float | None = None,
        max_value: float | None = None,
        coerce: bool = False
        ) -> None:
        self.min_value: float | None = min_value
        self.max_value: float | None = max_value
        self.coerce: bool = coerce
        
    def validate(self,value: Any) -> float:
        if self.coerce and not isinstance(value,float):
            try:
                value = float(value)
            except(ValueError, TypeError):
                raise ValidationError(
                    f"Could not convert {value!r} to float",
                    value=value
                )    
        
        if not isinstance(value, (int,float)) or isinstance(value,bool):
            raise ValidationError(
                f"Expected a float, got {type(value).__name__}.",
                value=value
            )
        
        value= float(value)
        
        if self.min_value is not None and value<self.min_value:
            raise ValidationError(
                f"Must be at least {self.min_value}",
                value=value,
            )
        
        if self.max_value is not None and value>self.max_value:
            raise ValidationError(
                f"Must be at most {self.max_value}",
                value=value
            )
        
        return value
    
    def __repr__(self) -> str:
        return (
            f"FloatValidator("
            f"min_value={self.min_value!r}, "
            f"max_value={self.max_value!r}, "
            f"coerce={self.coerce!r})"
        )

class BoolValidator(Validator):
    """ Validates that a value is boolean. 
    
    Parameters
    ----------
    coerce : bool
        If True, accept truthy strings like 'true', 'false', '1', '0'.
        Defaults to False.

    Example
    -------
        v = BoolValidator()
        v.validate(True)     # returns True
        v.validate("true")   # raises ValidationError unless coerce=True
    
    """
    
    # Accepted string values while coercing - 
    _TRUTH_VALUES: set[str] = {"true","1","yes"}
    _FALSE_VALUES: set[str] = {"false","0","no"}
    
    def __init__(self,*,coerce: bool = False) -> None:
        self.coerce: bool = coerce

    def validate(self, value: Any)-> bool:
        if self.coerce and isinstance(value,str):
            lowered: str = value.lower()
            if lowered in self._TRUTH_VALUES:
                return True
            if lowered in self._FALSE_VALUES:
                return False
            raise ValidationError(
                f"Cannot coerce {value!r} to boolean",
                value=value,
            )
        
        if not isinstance(value,bool):
            raise ValidationError(
                F"Expected a boolean, got {type(value).__name__}.",
                value=value,
            )
            
        return value
    
    def __repr__(self) -> str:
        return f"BoolValidator(coerce={self.coerce!r})"

class EmailValidator(Validator):
    """ Validates that a value is valid email address. 
    
    This validator checks format only — it does not send a confirmation
    email or verify the address exists. This is intentional: full email
    verification requires network access, which a validator should never do.

    Example
    -------
        v = EmailValidator()
        v.validate("alice@example.com")   # returns "alice@example.com"
        v.validate("not-an-email")        # raises ValidationError
    """
    
    # Email regex - 
    _EMAIL_REGEX: re.Pattern[str] = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )
    
    def validate(self,value: Any) -> str:
        if not isinstance(value,str):
            raise ValidationError(
                f"Expected a string, got {type(value).__name__}",
                value=value,
            )
        value = value.strip().lower()
        
        if not self._EMAIL_REGEX.match(value):
            raise ValidationError(
                f"{value!r} is not a valid email address",
                value=value,
            )
        
        return value
    
    def __repr__(self) -> str:
        return "EmailValidator()"
    
    