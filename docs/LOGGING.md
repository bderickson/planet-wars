# Logging in Planet Wars

## Overview

The game uses Python's built-in `logging` module with a custom setup that works in both browser (Pygbag) and desktop environments.

## Usage

### In any module:

```python
from game.logger import get_logger

# At module level
logger = get_logger(__name__)

# Then use it anywhere in the module
logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Warning messages")
logger.error("Error messages")
logger.critical("Critical errors")
```

### Log Levels

- `DEBUG`: Detailed information for diagnosing problems
- `INFO`: Confirmation that things are working as expected
- `WARNING`: Something unexpected happened, but the game continues
- `ERROR`: A more serious problem, some functionality failed
- `CRITICAL`: A serious error, the game may crash

### Changing Log Level

In `main.py`, change the level:

```python
setup_logging(level=logging.DEBUG)  # Very verbose
setup_logging(level=logging.INFO)   # Normal (default)
setup_logging(level=logging.WARNING)  # Quiet, only warnings and errors
```

### Browser Console

In the browser, logs automatically appear in:
- **Browser JavaScript console** (F12 → Console tab)
- **Python stdout** (captured by Pygbag)

The logger intelligently detects the platform and uses the appropriate output method.

### Example Output

```
12:34:56 [INFO] __main__: ============================================================
12:34:56 [INFO] __main__: Planet Wars starting...
12:34:56 [INFO] __main__: ============================================================
12:34:56 [INFO] __main__: Initializing Planet Wars game...
12:34:56 [DEBUG] __main__: Pygame initialized
12:34:56 [DEBUG] __main__: Screen created: 1200x800
12:34:56 [INFO] __main__: Platform: emscripten (browser: True)
12:34:56 [INFO] __main__: Initial state: start_screen
12:34:56 [DEBUG] __main__: Config and scoreboard loaded
12:34:56 [DEBUG] __main__: Menus initialized
12:34:56 [INFO] __main__: Game initialization complete
12:34:56 [INFO] __main__: Starting game loop
```

## Benefits

1. **Structured**: Organized by module name and log level
2. **Timestamps**: Know exactly when things happen
3. **Filterable**: Easy to find specific issues
4. **Cross-platform**: Works identically in browser and desktop
5. **Standard**: Uses Python's built-in `logging` module

