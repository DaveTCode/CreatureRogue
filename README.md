# CreatureRogue

[![Tests](https://github.com/DaveTCode/CreatureRogue/actions/workflows/tests.yml/badge.svg)](https://github.com/DaveTCode/CreatureRogue/actions/workflows/tests.yml)

## Requirements

### All system types
- Python 3.10+

### Unix OSs
Developing on Linux also requires SDL2 for the tcod library:
- `libsdl2-dev`

## Installation

```bash
pip install -e .[dev]
```

## Running the Game

After installation, you can run the game using:
```bash
creaturerogue
```

Or run directly:
```bash
python main.py
```

## Unit Testing

Tests run automatically via GitHub Actions on push and pull requests. To run tests locally:
```bash
pytest
```

## Linting

This project uses ruff for linting and formatting:
```bash
ruff check .        # Run linter
ruff format .       # Format code
ruff check --fix .  # Auto-fix issues
```

## Interactive Testing

There are some functional tests for the various components (e.g. the battle system) which 
consist of simple top level python applications that only invoke the parts of the main
application that are needed to run those areas. These are:

### Battle Testing
You can test the battle system by running:
```
python battle_test.py <pokedex#1> <level> <pokedex#2> <level> 
```

So for example, `python battle_test.py 1 50 4 50` will start a battle between a level 50
Charmander and a level 50 Bulbasaur.

### Pokedex Testing

You can test the pokedex view by running:
```
python pokedex_test.py
```
which will display a random pokedex (i.e. some creatures will be known, seen and unknown).