# Development

## Environment

```bash
python -m venv .venv
```

Activate the environment and install project requirements:

```bash
pip install -r requirements.txt
```

## Format Source

```bash
black fiscal
```

## Validate Python

```bash
python -m py_compile fiscal/__init__.py
```

## Build Documentation

```bash
mkdocs build --strict
```

## Preview Documentation

```bash
mkdocs serve
```

Open the local address shown by MkDocs, normally `http://127.0.0.1:8000/`.

## Test Coverage

Tests should cover:

- constructors and database queries
- every public method
- all twelve fiscal months
- all four fiscal quarters
- valid and invalid fiscal weeks
- leap and non-leap years
- actual and observed holiday paths
- reversed and nonintersecting ranges
- text and HTML calendar rendering
- date ranges crossing calendar years

## Release Validation

Before release:

```bash
python -m py_compile fiscal/__init__.py
pytest
mkdocs build --strict
```
