"""
valify.schema
~~~~~~~~~~~~~

The Schema class for validating dictionaries against a set of validators.

A Schema maps field names to Validator instances. When validate() is called,
each field in the data is run through its corresponding validator, and all
errors are collected before raising — so you get all errors at once, not
just the first one.
"""

from __future__ import annotations

from typing import Any

from .exceptions import ValidationError, RequiredFieldError, SchemaError
from .validators import OptionalValidator, Validator

class Schema(Validator):
    """ Validates a dictionary against a set of validators. 
    
    Parameters
    ----------
    fields : dict
        A mapping of field names to Validator instances.
    strict : bool
        If True, raise ValidationError for keys in the data that are
        not defined in the schema. Defaults to False.

    Example
    -------
        schema = Schema({
            "name": StringValidator(min_length=2),
            "age":  IntValidator(min_value=0, max_value=120),
        })

        result = schema.validate({"name": "Alice", "age": 30})
        print(result)  # {"name": "Alice", "age": 30}
    """
    
    def __init__(self,
                fields: dict[str, Validator],
                * ,
                strict: bool = False
                ) -> None:
        
        # Validate the schema definition itself before storing it.
        # This catches developer mistakes early, at schema creation time,
        # rather than mysteriously failing later at validation time.
        
        if not isinstance(fields,dict):
            raise SchemaError("Fields must be a dictionary")
        
        for key,val in fields.items():
            if not isinstance(key,str):
                raise SchemaError(
                    f"Field names must be string, got {type(key).__name__!r}."
                )
            if not isinstance(val,Validator):
                raise SchemaError(
                    f"Field {key!r} must be a Validator instance, "
                    f"got {type(val).__name__!r}."
                )
        
        self.fields: dict[str, Validator] = fields
        self.strict: bool = strict
        
    def validate(self,data: dict[str, Any]) -> dict[str, Any]:
        """ Validate a dictionary of data against the schema. 
        
        Parameters
        ----------
        data : dict
            The raw data to validate.

        Returns
        -------
        dict
            A new dictionary containing only the validated (and possibly
            coerced) values.

        Raises
        ------
        ValidationError
            If any field fails validation. Contains all errors at once.
        RequiredFieldError
            If a required field is missing from data.
        SchemaError
            If data is not a dictionary.
        """
        
        if not isinstance(data,dict):
            raise SchemaError(
                f"Expected a dictionary, got {type(data).__name__!r}"
            )
        
        errors: dict[str, Any] = {}
        result: dict[str, Any] = {}
        
        if self.strict:
            for key in data:
                if key not in self.fields:
                    errors[key] = f"Unknown field."
        
        for field_name,validator in self.fields.items():
            if field_name not in data:
                if isinstance(validator, OptionalValidator):
                    result[field_name] = validator.default
                else:
                    errors[field_name] = "Required field missing."
                continue
            
            try:
                result[field_name]=validator.validate(data[field_name])
            except ValidationError as e:
                errors[field_name]=e.message
        
        
        if errors:
            error_lines = "\n".join(
                f" {field}: {msg}" for field,msg in errors.items()
            )        
            raise ValidationError(
                f"Validation Failed:\n{error_lines}",
            )
        return result
        
        
    
    def __repr__(self) -> str:
        field_reprs = ", ".join(
            f"{k!r}: {v!r}" for k, v in self.fields.items()
        )
        return f"Schema({{{field_reprs}}}, strict={self.strict!r})"
    
    @classmethod
    def from_example(cls, example: dict[str, Any]) -> "Schema":
        """
        Generate a Schema automatically from a sample data dictionary.

        Inspects the type of each value and maps it to the appropriate
        validator. Supports nested dictionaries recursively.

        Parameters
        ----------
            example : dict
                A sample dictionary representing the expected data shape.

        Returns
        -------
        Schema
            A Schema instance with inferred validators.

        Example
        -------
            schema = Schema.from_example({
                "name":   "Alice",
                "age":    30,
                "email":  "alice@example.com",
                "score":  9.5,
                "active": True,
            })
            schema.validate({
                "name":   "Bob",
                "age":    25,
                "email":  "bob@example.com",
                "score":  8.0,
                "active": False,
            })
        """
        from .validators import (
            StringValidator,
            IntValidator,
            FloatValidator,
            BoolValidator,
            EmailValidator,
            ListValidator,
        )
        import re
        
        _EMAIL_RE = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        )
        
        fields: dict[str, Validator] = {}
        
        for key, value in example.items():
            if isinstance(value, bool):
                # bool must be checked first as bool is a subclass of int
                fields[key] = BoolValidator()
                
            elif isinstance(value, int):
                fields[key] = IntValidator()
                
            elif isinstance(value, float):
                fields[key] = FloatValidator()
                
            elif isinstance(value, str):
                if _EMAIL_RE.match(value.strip().lower()):
                    fields[key] = EmailValidator()
                else:
                    fields[key] = StringValidator()
            
            elif isinstance(value, dict):
                fields[key] = cls.from_example(value)
                
            elif isinstance(value, list) and value:
                # use the first item to infer the item validator
                item_example = {key:value[0]}
                item_schema = cls.from_example(item_example)
                item_validator = item_schema.fields[key]
                fields[key] = ListValidator(item_validator)
                
            else:
                # Fallback to StringValidator for unknown types
                fields[key] = StringValidator()
                
        return cls(fields)
                
       
    
