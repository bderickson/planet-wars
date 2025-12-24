# Planet Wars 🌍🚀

[![Tests](https://github.com/bderickson/planet-wars/actions/workflows/tests.yml/badge.svg)](https://github.com/bderickson/planet-wars/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/bderickson/planet-wars/branch/main/graph/badge.svg)](https://codecov.io/gh/bderickson/planet-wars)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/bderickson/planet-wars/pulls)

A browser-based space strategy game built with Python, Pygame, and Pygbag. Conquer the galaxy by capturing planets, building fleets, and outmaneuvering your AI opponent!

## 🌐 Play Online

**[Play Planet Wars →](https://planet-wars.derickson.me)**

Or run locally (see [Quick Start](#-quick-start) below)

## 🎮 Game Features

### Core Gameplay
- **Strategic Planet Conquest**: Click planets to select and send fleets to capture territory
- **Dynamic Ship Production**: Larger planets produce 1-4 ships per second
- **Real-time Combat**: Ships automatically battle when reaching enemy planets
- **Fleet Management**: Use the slider to control exactly how many ships to send
- **Victory Conditions**: Capture all enemy planets to win, or lose everything to defeat

### Strategic Abilities (One-Time Use)
- **🔄 Recall**: Instantly return all your fleets to their origin planets
- **⚡ Production Surge**: Double ship production on all planets for 10 seconds
- **🛡️ Shield Generator**: Reduce incoming damage by 50% on a planet for 15 seconds

### AI Opponent
- **Three Difficulty Levels**:
  - **Easy**: Slow, cautious, targets closest planets
  - **Medium**: Balanced strategy with moderate aggression
  - **Hard**: Fast decisions, 70% aggression, uses abilities strategically, prioritizes high-production planets

### Map Sizes
- **Small**: 7 planets - Quick skirmishes
- **Medium**: 13 planets - Balanced gameplay
- **Large**: 19 planets - Epic battles

**Games typically take between 1 and 5 minutes.**

### Audio System
Three distinct sound packs to choose from:
- **Default**: Space-themed sci-fi sounds
- **Classical**: Rachmaninoff and Beethoven for conquest and defeat
- **Silly**: Cartoon sound effects (BONK! BOING!)

### Game Modes
- **Scoreboard**: Track your best games with persistent high scores
- **Statistics**: View planets controlled, ships produced, battles won/lost
- **Scoring System**: Base 100 points, penalties for losses, bonuses for fast victories

## 🚀 Quick Start

### Installation

```bash
# Install pipenv if you don't have it
pip install pipenv

# Install project dependencies
pipenv install

# Activate the virtual environment
pipenv shell
```

### Run Locally (Desktop)

```bash
python main.py
```

### Build for Web (Browser)

```bash
# Build and test locally
pipenv run pygbag main.py

# This starts a local server at http://localhost:8000
# The game will run in your browser
```

## 🎯 How to Play

1. **Start a New Game**: Enter your name and configure your game settings
2. **Select a Planet**: Click one of your blue planets
3. **Send a Fleet**: 
   - Adjust the slider to choose how many ships to send
   - Click a target planet (enemy red or neutral gray)
4. **Use Abilities Wisely**: Each ability can only be used once per game
5. **Strategic Tips**:
   - Larger planets = more ship production
   - Shield your high-production planets when under attack
   - Use Production Surge when you control multiple large planets
   - Recall can save your fleets from a losing battle

### 🏆 Scoring System

Your score is based on **tactical performance** and **speed**:

**Final Score = Tactical Score + Time Bonus**

#### Tactical Penalties
Start with 100 points, lose points for mistakes:
- **Lost Battle** (attack repelled): -5 points
- **Lost Planet** (conquered by enemy): -10 points
- **Minimum Tactical Score**: 0

#### Time Bonuses
Fast victories are rewarded:
- **Under 60 seconds**: +50 bonus (Perfect speedrun! ⚡)
- **Under 2 minutes**: +30 bonus (Very fast 🚀)
- **Under 3 minutes**: +15 bonus (Fast ⏱️)
- **Under 5 minutes**: +5 bonus (Moderate 🐢)
- **5+ minutes**: No time bonus

#### Score Range
- **Maximum Score**: 150 (100 tactical + 50 time bonus)
- **Perfect Game**: 150 points (no losses, under 60 seconds)
- **Defeat**: 0 points (always)

**Strategy Tips:**
- Speed matters! Fast victories can offset tactical mistakes
- Each lost battle costs 5 points, lost planets cost 10
- Use Shield ability to prevent costly planet losses
- Balance risk vs speed - 60s, 120s, 180s, and 300s are critical time breakpoints

## 📁 Project Structure

```
planet_wars/
├── main.py                  # Entry point and game loop
├── game/
│   ├── game_state.py        # Core game logic and state management
│   ├── entities.py          # Planet and Ship classes
│   ├── renderer.py          # All drawing and UI rendering
│   ├── input_handler.py     # Mouse/keyboard input handling
│   ├── abilities.py         # Special ability system
│   ├── config.py            # Configuration and persistence
│   ├── scoreboard.py        # High score tracking
│   ├── game_over.py         # Victory/defeat screen
│   ├── sound.py             # Sound system management
│   ├── logger.py            # Cross-platform logging
│   ├── ai/
│   │   ├── base_ai.py       # AI interface
│   │   └── simple_ai.py     # Strategic AI implementation
│   ├── sound_plugins/
│   │   ├── base_sound_plugin.py    # Sound plugin interface
│   │   ├── default_plugin.py       # Space-themed sounds
│   │   ├── classical_plugin.py     # Classical music
│   │   └── silly_plugin.py         # Cartoon sounds
│   └── menus/
│       ├── base_menu.py     # Shared menu functionality
│       ├── menu.py          # Main menu
│       ├── game_config_menu.py     # Game configuration
│       └── scoreboard_menu.py      # High scores display
├── assets/
│   └── audio/
│       ├── mp3/             # Audio files for desktop
│       ├── ogg/             # Audio files for browser (OGG Vorbis)
│       ├── generate_default_sounds.py   # Generate default sounds
│       ├── generate_silly_sounds.py     # Generate silly sounds
│       ├── convert_to_ogg.py            # MP3 to OGG conversion
│       └── trim_audio.py                # Audio trimming utility
├── tests/
│   ├── unit/                # Unit tests for all modules
│   └── integration/         # Integration tests
├── files/                   # Local data storage (gitignored)
│   └── README.md
├── docs/                    # Documentation
│   ├── BROWSER_DEPLOYMENT.md
│   └── SOUND_SYSTEM.md
├── Pipfile                  # Dependency management
└── README.md
```

## 🧪 Testing

```bash
# Run all tests
pipenv run pytest

# Run with coverage
pipenv run pytest --cov=game --cov-report=html

# Run specific test file
pipenv run pytest tests/unit/test_game_state.py -v

# Run integration tests
pipenv run pytest tests/integration/ -v
```

Current test coverage: 300+ tests across all modules

## 🛠️ Development

### Code Quality

```bash
# Run linter
pipenv run pytest --pylint

# Check specific files
pipenv run pylint game/game_state.py
```

### Audio Generation

```bash
# Generate default space sounds
cd assets/audio
pipenv run python generate_default_sounds.py

# Generate silly cartoon sounds
pipenv run python generate_silly_sounds.py

# Trim audio files (MP3 input, creates both MP3 and OGG)
pipenv run python trim_audio.py path/to/file.mp3 7  # Trim to 7 seconds

# Convert all MP3s to OGG for browser compatibility
pipenv run python convert_to_ogg.py
```

## 📚 Documentation

- [Sound System](docs/SOUND_SYSTEM.md) - Audio plugin architecture

## 🎓 Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pygbag Documentation](https://pygame-web.github.io/)
- [Pygame Tutorial](https://www.pygame.org/wiki/tutorials)

## 🙏 Acknowledgments

- Lucas - His ideas, help, and enthusiasm helped make this game what it is
- Built with assistance from Cursor AI
- Audio processing using pydub and pygame
- Classical music: Rachmaninoff's Prelude in C-sharp minor, Beethoven's Symphony No. 5

---

**Enjoy conquering the galaxy!** 🌌👾🚀
