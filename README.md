# CreatureRogue [![Build Status](https://travis-ci.org/DaveTCode/CreatureRogue.svg?branch=develop)](https://travis-ci.org/DaveTCode/CreatureRogue) [![Coverage Status](https://coveralls.io/repos/DaveTCode/CreatureRogue/badge.svg?branch=develop&service=github)](https://coveralls.io/github/DaveTCode/CreatureRogue?branch=develop)

## Requirements

### All system types
- `Python 3.6`

### Unix OSs
Developing on linux also requires the following packages for building libtcod-cffi from source:
- `gcc`
- `libsdl2-dev`
- `libffi-dev`
- `python-dev`

Once those dependencies are installed then run the following command (system independent) to
install the python dependencies.
```
pip install -r requirements.txt
```

which should be installed before attempting to run `pip install`.

## Unit Testing

All unit tests are run on all branches on push and the results are on [Travis CI](https://travis-ci.org/DaveTCode/CreatureRogue)
, if you want to run the tests locally you can use
```
py.test --cov=CreatureRogue tests/
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