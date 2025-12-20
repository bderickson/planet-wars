# Logging Added Throughout Game Code

## Summary

Added comprehensive logging to key game modules for easier debugging and troubleshooting.

## Modules Updated

### 1. **main.py**
- Set default log level to `DEBUG`
- Logs at game initialization, state transitions, and major events

### 2. **game/game_state.py**
- Initialization logging with map size, AI difficulty, sound pack
- Map generation logging (planet count, placement)
- Fleet operations (sending ships, validation)
- Victory/defeat conditions
- Game statistics

### 3. **game/config.py**
- Configuration loading (file vs localStorage)
- Player name loading/saving
- Error handling for corrupted configs

### 4. **game/scoreboard.py**
- Scoreboard initialization
- Score entries being added
- Loading/saving operations

### 5. **game/sound.py**
- Sound manager initialization
- Sound plugin loading
- Mixer setup

## Log Levels Used

- **DEBUG**: Detailed information (initialization steps, internal state)
- **INFO**: Major game events (game started, victory, defeat, scores)
- **WARNING**: Unexpected but recoverable situations (no ships to send, config load failed)
- **ERROR**: Not currently used, but available for serious issues

## Example Output

```
12:34:56 [INFO] __main__: ============================================================
12:34:56 [INFO] __main__: Planet Wars starting...
12:34:56 [INFO] __main__: ============================================================
12:34:56 [INFO] __main__: Initializing Planet Wars game...
12:34:56 [DEBUG] __main__: Pygame initialized
12:34:56 [DEBUG] __main__: Screen created: 1200x800
12:34:56 [INFO] __main__: Platform: emscripten (browser: True)
12:34:56 [DEBUG] game.config: Config initializing (browser: True)
12:34:56 [DEBUG] game.config: Loading config from localStorage
12:34:56 [INFO] game.config: Config loaded: player_name=Player
12:34:56 [DEBUG] game.scoreboard: Scoreboard initializing (browser: True)
12:34:56 [INFO] game.scoreboard: Scoreboard loaded: 5 scores
12:34:56 [INFO] __main__: Starting new game: map=medium, difficulty=medium, sound=default
12:34:56 [INFO] game.game_state: Initializing GameState: map=medium, ai=medium, sound=default
12:34:56 [DEBUG] game.game_state: Abilities initialized
12:34:56 [INFO] game.game_state: Generating map: size=medium
12:34:56 [DEBUG] game.game_state: Target planet count: 9
12:34:56 [INFO] game.sound: Initializing SoundManager: plugin=default
12:34:56 [DEBUG] game.sound: Sound plugin loaded: DefaultSoundPlugin
12:34:57 [DEBUG] game.game_state: Sending fleet: 10 ships from Earth to Mars
12:35:10 [INFO] game.game_state: VICTORY: Enemy has no planets or ships
```

## Changing Log Level

In `main.py`, change this line:

```python
setup_logging(level=logging.DEBUG)  # Very verbose
setup_logging(level=logging.INFO)   # Normal
setup_logging(level=logging.WARNING)  # Quiet
```

## Next Steps

When troubleshooting browser issues:
1. Open browser console (F12)
2. Look for the structured log output
3. Find exactly where things break
4. Add more DEBUG logging if needed in specific areas

