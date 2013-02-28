import libtcodpy as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
TITLE = 'Creature Rogue'

FONT = 'arial10x10.png'

DB_FILE = 'pokedex.db3'

# Colors
LINE_COLOR = libtcod.Color(255, 255, 255)
BATTLE_TEXT_COLOR = libtcod.Color(255, 255, 255)
GOOD_HEALTH_COLOR = libtcod.Color(0, 255, 0)
HALF_HEALTH_COLOR = libtcod.Color(255, 255, 0)
LOW_HEALTH_COLOR = libtcod.Color(255, 0, 0)
BLANK_HEALTH_COLOR = libtcod.Color(60, 60, 60)