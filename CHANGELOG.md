# Changelog

All notable changes to valify will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-05-29

### Added
- Nested schema support — `Schema` now inherits from `Validator`
  and can be used as a field value inside another `Schema`
- 4 new tests for nested schema validation (54 total)

## [0.3.0] - 2026-05-27

### Added
- `OptionalValidator` — makes any field optional with a default value
- `ListValidator` — validates every item in a list
- `EnumValidator` — value must be one of a fixed set of choices
- 12 new tests (50 total)

## [0.2.0] - 2026-05-27

### Added
- Full type hints across all modules (exceptions, validators, schema)
- mypy compatibility — passes strict type checking

## [0.1.0] - 2026-05-24

### Added
- `StringValidator` — validates strings with optional min/max length
- `IntValidator` — validates integers with optional min/max value
- `FloatValidator` — validates floats with optional min/max value
- `BoolValidator` — validates booleans with optional string coercion
- `EmailValidator` — validates email address format
- `Schema` — validates dictionaries against a set of validators
- Custom exception hierarchy: `ValifyError`, `ValidationError`,
  `RequiredFieldError`, `SchemaError`
- 38 tests covering all validators and schema behaviour