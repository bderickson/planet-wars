# Planet Wars

A browser-based space strategy game built with Python, Pygame, and Pygbag.

## Setup

### Install Dependencies

```bash
# Install pipenv if you don't have it
pip install pipenv

# Install project dependencies
pipenv install

# Activate the virtual environment
pipenv shell
```

### Run Locally

```bash
python main.py
```

## Gameplay (Current)

- Click on a blue planet to select it
- Click on another planet to send half your ships there
- Planets slowly produce ships over time
- Goal: Capture all planets (combat system coming soon!)

## Project Structure

```
planet_wars/
├── main.py              # Entry point and game loop
├── game/
│   ├── __init__.py
│   ├── game_state.py    # Game state management
│   ├── entities.py      # Game entities (Planet, Ship)
│   ├── renderer.py      # All drawing/rendering logic
│   └── input_handler.py # Mouse/keyboard input
├── assets/              # Future: images, sounds
├── Pipfile              # Dependency management
└── README.md
```

## Building for Web (Browser)

```bash
# Make sure you're in the pipenv shell
pipenv shell

# Build for web
pygbag main.py

# This will create a build/ folder
# You can test it by running the local server pygbag starts
# Or upload the build folder to GitHub Pages, itch.io, etc.
```

## Development Tips

### Working with Cursor

1. **Ask for specific features**: "Add collision detection between ships and planets"
2. **Use TODO comments**: Add `# TODO: implement combat system` - Cursor can see these
3. **Iterate incrementally**: Build one feature at a time
4. **Keep files focused**: Each file has one clear responsibility

### Code Formatting

```bash
# Format code with black
pipenv run black .

# Lint code
pipenv run pylint game/
```

## Next Features to Build

- [ ] Combat system (ships fight when reaching enemy planets)
- [ ] AI opponent
- [ ] Win/lose conditions
- [ ] Multiple levels
- [ ] Sound effects
- [ ] Particle effects for explosions
- [ ] Better ship visuals (formations, trails)
- [ ] Save/load game state

## Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pygbag Documentation](https://pygame-web.github.io/)
- [Pygame Tutorial](https://www.pygame.org/wiki/tutorials)

