# Planet Wars Documentation

## Game Documentation

### [Logging System](LOGGING.md)
How to use the logging system in both browser and desktop environments.

### [Scoreboard System](SCOREBOARD_SYSTEM.md)
Details about the high score tracking and scoring mechanics.

### [Sound System](SOUND_SYSTEM.md)
Documentation for the pluggable sound system and available sound packs.

### [Browser Deployment](BROWSER_DEPLOYMENT.md)
Guide for deploying the game to the browser using Pygbag, including GitHub Pages and Itch.io.

---

## Quick Start

### Running Locally
```bash
# Install dependencies
pipenv install

# Run the game
pipenv run python main.py
```

### Building for Browser
```bash
# Build and test locally
pipenv run pygbag main.py

# Browser will open at http://localhost:8000
```

---

## Project Structure

```
planet_wars/
├── main.py                 # Entry point
├── game/                   # Game modules
│   ├── game_state.py       # Core game logic
│   ├── renderer.py         # Graphics rendering
│   ├── input_handler.py    # Input processing
│   ├── entities.py         # Planet & Ship classes
│   ├── abilities.py        # Player abilities
│   ├── config.py           # Configuration management
│   ├── scoreboard.py       # High score tracking
│   ├── logger.py           # Logging utility
│   ├── sound.py            # Sound manager
│   ├── ai/                 # AI implementations
│   ├── menus/              # Menu screens
│   └── sound_plugins/      # Sound pack plugins
├── assets/                 # Game assets
│   └── audio/              # Sound files & generators
├── tests/                  # Unit & integration tests
└── docs/                   # Documentation (you are here!)
```

---

## Testing

```bash
# Run all tests
pipenv run pytest

# Run with coverage
pipenv run pytest --cov=game

# Run specific test file
pipenv run pytest tests/unit/test_scoreboard.py
```

---

## Key Features

- ✅ Real-time strategy gameplay
- ✅ AI opponents with difficulty levels
- ✅ Multiple map sizes
- ✅ Special abilities (Recall, Production Surge, Shield)
- ✅ Three sound packs (Default, Classical, Silly)
- ✅ Persistent high scores
- ✅ Browser and desktop support
- ✅ Comprehensive test suite

