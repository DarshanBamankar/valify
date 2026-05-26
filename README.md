[![PyPI version](https://badge.fury.io/py/valify.svg)](https://pypi.org/project/valify/)
[![Python](https://img.shields.io/pypi/pyversions/valify.svg)](https://pypi.org/project/valify/)

# valify

A composable, expressive data validation library for Python.

## Installation

```bash
pip install valify
```

## Quick Start

```python
from valify import Schema, StringValidator, IntValidator, EmailValidator

schema = Schema({
    "name":  StringValidator(min_length=2, max_length=50),
    "age":   IntValidator(min_value=0, max_value=120),
    "email": EmailValidator(),
})

# Valid data — returns cleaned, validated dictionary
result = schema.validate({
    "name":  "Alice",
    "age":   30,
    "email": "alice@example.com",
})
print(result)
# {'name': 'Alice', 'age': 30, 'email': 'alice@example.com'}

# Invalid data — raises ValidationError with ALL errors at once
schema.validate({
    "name":  "A",
    "age":   -5,
    "email": "not-an-email",
})
# ValidationError: Validation failed:
#   name: Must be at least 2 characters long.
#   age: Must be at least 0.
#   email: 'not-an-email' is not a valid email address.
```

## Validators

| Validator | What it checks |
|-----------|---------------|
| `StringValidator` | Strings, with optional min/max length |
| `IntValidator` | Integers, with optional min/max value |
| `FloatValidator` | Floats, with optional min/max value |
| `BoolValidator` | Booleans, with optional string coercion |
| `EmailValidator` | Email address format |

## Validators in Detail

### StringValidator

```python
from valify import StringValidator

v = StringValidator(
    min_length=2,   # minimum character length
    max_length=50,  # maximum character length
    strip=True,     # strip whitespace before validating (default: True)
)
```

### IntValidator

```python
from valify import IntValidator

v = IntValidator(
    min_value=0,    # minimum allowed value
    max_value=120,  # maximum allowed value
    coerce=False,   # if True, converts "42" -> 42 (default: False)
)
```

### EmailValidator

```python
from valify import EmailValidator

v = EmailValidator()
v.validate("alice@example.com")  # returns "alice@example.com"
```

## Using Validators Standalone

Validators work without a Schema too:

```python
from valify import IntValidator
from valify.exceptions import ValidationError

v = IntValidator(min_value=0)

try:
    v.validate(-1)
except ValidationError as e:
    print(e.message)  # Must be at least 0.
    print(e.value)    # -1
```

## Error Handling

```python
from valify.exceptions import (
    ValifyError,        # base — catches everything
    ValidationError,    # a value failed validation
    RequiredFieldError, # a required field was missing
    SchemaError,        # the schema definition is invalid
)
```

## License

MIT