# Pluggable Sound System

## Overview
The Planet Wars game now features a pluggable sound system that allows different sound packs to be selected from the game configuration menu.

## Architecture

### Base Plugin
- **`game/sound_plugins/base_sound_plugin.py`**: Abstract base class defining the sound plugin interface
- Methods:
  - `attack_succeeded()`: Sound when planet is conquered
  - `attack_failed()`: Sound when attack fails
  - `fleet_launched()`: Sound when fleet launches
  - `game_victory()`: Optional sound for winning
  - `game_defeat()`: Optional sound for losing
  - `cleanup()`: Optional cleanup method

### Available Plugins

#### 1. Default Plugin (`default_plugin.py`)
- **Conquest**: Rachmaninoff's Prelude in C-sharp minor (7 seconds from MP3 file, or procedurally generated fallback)
- **Attack Failed**: Heavy explosion with noise and rumble
- **Fleet Launch**: Ascending swoosh sound

#### 2. Classical Plugin (`classical_plugin.py`)
- **Conquest**: Triumphant trumpet-style fanfare (C-E-G-C progression)
- **Attack Failed**: Dramatic diminished chord crash
- **Fleet Launch**: Ascending harp glissando

#### 3. Silly Plugin (`silly_plugin.py`)
- **Conquest**: Cartoon victory jingle with vibrato
- **Attack Failed**: Comic bonk/hit sound
- **Fleet Launch**: Spring boing sound with dampened oscillation

## Usage

### In Game
1. Go to Game Configuration menu
2. Select desired sound pack (Default, Classical, or Silly)
3. Start game

### In Code

```python
from game.sound_plugins import create_sound_plugin

# Create a plugin
plugin = create_sound_plugin("classical")

# Use plugin methods
plugin.attack_succeeded()
plugin.attack_failed()
plugin.fleet_launched()
```

### Sound Manager
The `SoundManager` class wraps the plugin system:

```python
from game.sound import SoundManager

sound_manager = SoundManager(plugin_name="silly")
sound_manager.play_attack_succeeded()
sound_manager.play_attack_failed()
sound_manager.play_fleet_launched()

# Change plugin on the fly
sound_manager.change_plugin("classical")
```

## Adding New Plugins

1. Create a new file in `game/sound_plugins/` (e.g., `my_plugin.py`)
2. Inherit from `BaseSoundPlugin`
3. Implement all required methods
4. Register in `game/sound_plugins/__init__.py`
5. Add to game configuration menu

Example:
```python
from game.sound_plugins.base_sound_plugin import BaseSoundPlugin

class MyPlugin(BaseSoundPlugin):
    def __init__(self):
        super().__init__()
        # Initialize sounds
    
    def attack_succeeded(self):
        # Play conquest sound
        pass
    
    def attack_failed(self):
        # Play failure sound
        pass
    
    def fleet_launched(self):
        # Play launch sound
        pass
    
    def game_victory(self):
        pass
    
    def game_defeat(self):
        pass
```

## Files Modified
- `game/sound.py`: Now uses plugin system
- `game/game_state.py`: Accepts `sound_pack` parameter
- `game/game_config_menu.py`: Added Sound Pack selection UI
- `main.py`: Passes sound_pack to GameState

## Files Added
- `game/sound_plugins/__init__.py`: Plugin factory
- `game/sound_plugins/base_sound_plugin.py`: Abstract base class
- `game/sound_plugins/default_plugin.py`: Default sounds (Rachmaninoff)
- `game/sound_plugins/classical_plugin.py`: Classical music sounds
- `game/sound_plugins/silly_plugin.py`: Comedic sounds

