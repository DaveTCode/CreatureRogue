"""
Configurable settings for the application.
"""

import tcod as libtcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
FPS_LIMIT = 30
TITLE = 'Creature Rogue'

FONT = 'terminal16x16_gs_ro.png'

DB_FILE = 'pokedex.db3'
LOCATION_AREA_RECTS_FILE = 'location_area_rects.txt'

# Colors
BACKGROUND_COLOR = libtcod.Color(0, 0, 0)
FOREGROUND_COLOR = libtcod.white
LINE_COLOR = libtcod.white
LEVEL_UP_BG_COLOR = libtcod.Color(50, 50, 50)
MENU_BG_COLOR = libtcod.Color(50, 50, 50)
CATCH_GRAPHIC_BG_COLOR = libtcod.Color(50, 50, 50)
BATTLE_TEXT_COLOR = libtcod.white
GOOD_HEALTH_COLOR = libtcod.Color(0, 255, 0)
HALF_HEALTH_COLOR = libtcod.Color(255, 255, 0)
LOW_HEALTH_COLOR = libtcod.Color(255, 0, 0)
BLANK_HEALTH_COLOR = libtcod.Color(60, 60, 60)
POKEDEX_UNKNOWN_COLOR = libtcod.Color(90, 90, 90)
POKEDEX_SEEN_COLOR = libtcod.Color(0, 0, 255)
POKEDEX_KNOWN_COLOR = libtcod.Color(0, 255, 0)
POKEDEX_LINE_COLOR = libtcod.white
PLAYER_COLOR = libtcod.yellow

LOCAL_LANGUAGE_ID = 9  # English
VERSION_GROUP_ID = 6  # Emerald
POKEDEX_ID = 1  # Entire national dex
VERSION_ID = 7  # Flavor text version. Set this to 1 for original 151 pokemon.
LOCATION_GENERATION_ID = 4  # Can be 4 or 5 (Gen 4 or 5 apparently)
