"""
Tests for valify.schema
"""

import pytest
from valify import (
    Schema,
    StringValidator,
    IntValidator,
    EmailValidator,
    ValidationError,
    SchemaError,
)
from valify.validators import BoolValidator

class TestSchemaValidation:
    """Tests for Schema.validate()"""

    def setup_method(self):
        # setup_method runs before EVERY test in this class.
        # We define a reusable schema here so we don't repeat
        # ourselves in every single test.
        self.schema = Schema({
            "name":  StringValidator(min_length=2),
            "age":   IntValidator(min_value=0, max_value=120),
            "email": EmailValidator(),
        })

    def test_valid_data_returns_dict(self):
        result = self.schema.validate({
            "name":  "Alice",
            "age":   30,
            "email": "alice@example.com",
        })
        assert result == {
            "name":  "Alice",
            "age":   30,
            "email": "alice@example.com",
        }

    def test_multiple_errors_raised_at_once(self):
        with pytest.raises(ValidationError) as exc_info:
            self.schema.validate({
                "name":  "A",
                "age":   -1,
                "email": "bad",
            })
        error_message = str(exc_info.value)
        assert "name" in error_message
        assert "age" in error_message
        assert "email" in error_message

    def test_missing_field_raises_error(self):
        with pytest.raises(ValidationError) as exc_info:
            self.schema.validate({"name": "Alice"})
        error_message = str(exc_info.value)
        assert "age" in error_message
        assert "email" in error_message

    def test_non_dict_raises_schema_error(self):
        with pytest.raises(SchemaError):
            self.schema.validate("not a dict")

    def test_extra_fields_ignored_by_default(self):
        result = self.schema.validate({
            "name":  "Alice",
            "age":   30,
            "email": "alice@example.com",
            "extra": "ignored",
        })
        assert "extra" not in result


class TestSchemaDefinition:
    """Tests for Schema creation and validation of schema itself."""

    def test_invalid_field_name_raises_schema_error(self):
        with pytest.raises(SchemaError):
            Schema({123: IntValidator()})

    def test_non_validator_value_raises_schema_error(self):
        with pytest.raises(SchemaError):
            Schema({"name": "not a validator"})

    def test_non_dict_fields_raises_schema_error(self):
        with pytest.raises(SchemaError):
            Schema("not a dict")

    def test_strict_mode_rejects_extra_fields(self):
        schema = Schema(
            {"name": StringValidator()},
            strict=True,
        )
        with pytest.raises(ValidationError):
            schema.validate({"name": "Alice", "extra": "field"})

class TestNestedSchemas:
    """ Tests for Nested Schemas Validation. """
    
    def setup_method(self):
        address_schema = Schema({
            "street": StringValidator(min_length=2),
            "city": StringValidator(min_length=2),
            "pin": StringValidator(min_length=6, max_length=6),
        })
        
        self.schema = Schema({
            "name": StringValidator(min_length=2),
            "age": IntValidator(min_value=0),
            "address": address_schema,
        })
        
        self.nested_schema = Schema({
            "user": self.schema,
            "allowed": BoolValidator(),
        })
        
    def test_valid_nested_data(self):
        result = self.schema.validate({
            "name": "Darshan",
            "age": 21,
            "address": {
                "street": "MG road",
                "city": "Pune",
                "pin": "412458",
            }
        })
        assert result["address"]["city"] == "Pune"
    
    def test_invalid_nested_field_reports_error(self):
        with pytest.raises(ValidationError):
            result = self.schema.validate({
                "name": "Darshan",
                "age": 21,
                "address": {
                    "street": "M",
                    "city": "Pune",
                    "pin": "412458",
                }
            })
    
    def test_missing_nested_field_reports_error(self):
        with pytest.raises(ValidationError):
            result = self.schema.validate({
                "name": "Darshan",
                "age": 21,
                "address": {
                    "city": "Pune",
                    "pin": "412458",
                }
            })
            
    def test_deeply_nested_schemas(self):
        result = self.nested_schema.validate({
            "user": {
                "name": "Darshan",
                "age": 21,
                "address": {
                    "street": "MG road",
                    "city": "Pune",
                    "pin": "412568",
                }
            },
            "allowed": True
            
        })
        assert result["user"]["address"]["city"] == "Pune"