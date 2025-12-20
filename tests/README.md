# Tests for Planet Wars

This directory contains unit and integration tests for the Planet Wars game.

## Running Tests

### Run all tests
```bash
pipenv run pytest
```

### Run with coverage report
```bash
pipenv run pytest --cov=game --cov-report=html
```

### Run specific test file
```bash
pipenv run pytest tests/unit/test_entities.py
```

### Run tests with verbose output
```bash
pipenv run pytest -v
```

### Run tests and stop on first failure
```bash
pipenv run pytest -x
```

## Test Organization

- `tests/unit/` - Unit tests for individual components
- `tests/integration/` - Integration tests for multiple components working together

## Writing Tests

Example unit test structure:

```python
import pytest
from game.entities import Planet

def test_planet_creation():
    planet = Planet(100, 100, 20, owner="Player")
    assert planet.x == 100
    assert planet.y == 100
    assert planet.owner == "Player"

def test_planet_production():
    planet = Planet(100, 100, 20, owner="Player")
    planet.update(1.0)  # 1 second
    assert planet.ship_count > 0
```

## Coverage Reports

After running tests with `--cov-report=html`, open `htmlcov/index.html` in your browser to see detailed coverage reports.

