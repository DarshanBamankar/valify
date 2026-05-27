"""
Tests for valify.validators
"""

import pytest
from valify import (
    StringValidator,
    IntValidator,
    FloatValidator,
    BoolValidator,
    EmailValidator,
    ValidationError,
)
from valify.validators import EnumValidator, ListValidator, OptionalValidator 

class TestStringValidator:
    """ Tests for StringValidator. """
    
    def test_valid_string(self):
        v = StringValidator()
        assert v.validate("hello") == "hello"
    
    def test_strips_whitespaces(self):
        v = StringValidator()
        assert v.validate(" hello ") == "hello"
    
    def test_min_length_passes(self):
        v = StringValidator(min_length=2)
        assert v.validate("hi") == "hi"
    
    def test_min_length_fails(self):
        v = StringValidator(min_length=2)
        with pytest.raises(ValidationError):
            v.validate("h")
    
    def test_max_length_passes(self):
        v = StringValidator(max_length=5)
        assert v.validate("hello") == "hello"
        
    def test_max_length_fails(self):
        v = StringValidator(max_length=5)
        with pytest.raises(ValidationError):
            v.validate("toolongstring")

    def test_wrong_type(self):
        v = StringValidator()
        with pytest.raises(ValidationError):
            v.validate(123)

class TestIntValidator:
    """Tests for IntValidator."""

    def test_valid_int(self):
        v = IntValidator()
        assert v.validate(42) == 42

    def test_min_value_fails(self):
        v = IntValidator(min_value=0)
        with pytest.raises(ValidationError):
            v.validate(-1)

    def test_max_value_fails(self):
        v = IntValidator(max_value=100)
        with pytest.raises(ValidationError):
            v.validate(101)

    def test_bool_rejected(self):
        v = IntValidator()
        with pytest.raises(ValidationError):
            v.validate(True)

    def test_coerce_string_to_int(self):
        v = IntValidator(coerce=True)
        assert v.validate("42") == 42

    def test_coerce_fails_on_invalid(self):
        v = IntValidator(coerce=True)
        with pytest.raises(ValidationError):
            v.validate("abc")


class TestEmailValidator:
    """Tests for EmailValidator."""

    def test_valid_email(self):
        v = EmailValidator()
        assert v.validate("alice@example.com") == "alice@example.com"

    def test_normalises_to_lowercase(self):
        v = EmailValidator()
        assert v.validate("Alice@Example.COM") == "alice@example.com"

    def test_invalid_email(self):
        v = EmailValidator()
        with pytest.raises(ValidationError):
            v.validate("not-an-email")

    def test_wrong_type(self):
        v = EmailValidator()
        with pytest.raises(ValidationError):
            v.validate(123)

class TestFloatValidator:
    """Tests for FloatValidator."""

    def test_valid_float(self):
        v = FloatValidator()
        assert v.validate(3.14) == 3.14

    def test_int_accepted_as_float(self):
        v = FloatValidator()
        assert v.validate(3) == 3.0

    def test_min_value_fails(self):
        v = FloatValidator(min_value=0.0)
        with pytest.raises(ValidationError):
            v.validate(-0.1)

    def test_max_value_fails(self):
        v = FloatValidator(max_value=1.0)
        with pytest.raises(ValidationError):
            v.validate(1.1)

    def test_bool_rejected(self):
        v = FloatValidator()
        with pytest.raises(ValidationError):
            v.validate(True)

    def test_coerce_string_to_float(self):
        v = FloatValidator(coerce=True)
        assert v.validate("3.14") == 3.14


class TestBoolValidator:
    """Tests for BoolValidator."""

    def test_valid_true(self):
        v = BoolValidator()
        assert v.validate(True) is True

    def test_valid_false(self):
        v = BoolValidator()
        assert v.validate(False) is False

    def test_int_rejected(self):
        v = BoolValidator()
        with pytest.raises(ValidationError):
            v.validate(1)

    def test_coerce_true_strings(self):
        v = BoolValidator(coerce=True)
        assert v.validate("yes") is True
        assert v.validate("1") is True
        assert v.validate("true") is True

    def test_coerce_false_strings(self):
        v = BoolValidator(coerce=True)
        assert v.validate("no") is False
        assert v.validate("0") is False
        assert v.validate("false") is False

    def test_coerce_invalid_string(self):
        v = BoolValidator(coerce=True)
        with pytest.raises(ValidationError):
            v.validate("maybe")

class TestOptionalValidator:
    """ Tests for Optional Validator. """
    
    def test_valid_value_passes(self):
        v = OptionalValidator(StringValidator(), default = "")
        assert v.validate("Hello") == "Hello"
    
    def test_none_returns_default(self):
        v = OptionalValidator(StringValidator(), default = "")
        assert v.validate(None) == ""
    
    def test_none_returns_none_default(self):
        v = OptionalValidator(StringValidator())
        assert v.validate(None) is None

class TestListValidator:
    """ Tests for List Validator. """
    
    def test_valid_value_passes(self):
        v = ListValidator(StringValidator())
        assert v.validate(["D","M"]) == ["D", "M"]
        
    def test_non_list_raises_error(self):
        v = ListValidator(StringValidator())
        with pytest.raises(ValidationError):
            v.validate("not a list")
    
    def test_below_min_items_raises_error(self):
        v = ListValidator(StringValidator(), min_items=2)
        with pytest.raises(ValidationError):
            v.validate(["Hello"])
    
    def test_above_max_items_raises_error(self):
        v = ListValidator(StringValidator(), max_items=2)
        with pytest.raises(ValidationError):
            v.validate(["1","2","3"])
    
    def test_invalid_item_inside_list(self):
        v = ListValidator(StringValidator())
        with pytest.raises(ValidationError):
            v.validate(["1",2,"3",4])

class TestEnumValidator:
    """Tests for Enum Validator. """
    
    def test_valid_choice_pass(self):
        v = EnumValidator(["admin", "user"])
        assert v.validate("admin") == "admin"
    
    def test_invalid_choice_raises_error(self):
        v = EnumValidator(["admin", "user"])
        with pytest.raises(ValidationError):
            v.validate("superadmin")
    
    def test_case_sensitive_mode_works_if_true(self):
        v = EnumValidator(["admin", "user"], case_sensitive=True)
        with pytest.raises(ValidationError):
            v.validate("Admin")
    
    def test_case_sensitive_mode_works_if_false(self):
        v = EnumValidator(["admin", "user"], case_sensitive=False)
        assert v.validate("Admin") == "Admin"
        
    