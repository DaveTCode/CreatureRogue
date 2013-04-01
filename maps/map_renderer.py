from __future__ import division
import libtcodpy as libtcod
import settings

class MapCell():

    def __init__(self, base_cell):
        self.base_cell = base_cell
    
    def color(self):
        return self.base_cell.display_color
        
    def char(self):
        return self.base_cell.display_char

class BaseMapCell():

    def __init__(self, identifier, display_char, display_color, cell_passable_type):
        self.identifier = identifier
        self.display_char = display_char
        self.display_color = display_color
        self.cell_passable_type = cell_passable_type

class MapRenderer():
    
    def __init__(self, game, console):
        self.game = game
        self.console = console
        self.start_x = self.start_y = 0
        
    def render(self, player):
        self._centre_map_on_player(player)
        self._render_map(player.map)
        self._render_player(player)

    def _centre_map_on_player(self, player):
        x, y = player.coords
        self.start_x = x - settings.SCREEN_WIDTH // 2
        self.start_y = y - settings.SCREEN_HEIGHT // 2
        
    def _render_player(self, player):
        x,y = player.coords
    
        libtcod.console_set_default_foreground(self.console, settings.PLAYER_COLOR)
        libtcod.console_put_char(self.console, x - self.start_x, y - self.start_y, '@')
    
    def _render_map(self, map):
        for y in range(self.start_y, self.start_y + settings.SCREEN_HEIGHT):
            for x in range(self.start_x, self.start_x + settings.SCREEN_WIDTH):
                if y >= 0 and y < len(map.tiles) and x >= 0 and x < len(map.tiles[y]):
                    cell = map.tiles[y][x]
                
                    libtcod.console_set_default_foreground(self.console, cell.color())
                    libtcod.console_put_char(self.console, x - self.start_x, y - self.start_y, cell.char())

# Passable cell types
BLOCK_CELL = 0
WATER_CELL = 1
EMPTY_CELL = 2

# Base cell types that maps can be made from
BRIDGE = BaseMapCell('', '-', libtcod.Color(255, 255, 0), EMPTY_CELL)
STATUE = BaseMapCell('', 'S', libtcod.Color(70, 70, 70), BLOCK_CELL)
PATH = BaseMapCell('', '-', libtcod.Color(255, 255, 255), EMPTY_CELL)
FENCE_HORIZONTAL = BaseMapCell('', 'X', libtcod.Color(139, 69, 19), BLOCK_CELL)
GRASS = BaseMapCell('', '.', libtcod.Color(255, 255, 255), EMPTY_CELL)
LETTERBOX = BaseMapCell('', 'L', libtcod.Color(100, 100, 100), BLOCK_CELL)
FLOWER = BaseMapCell('', '.', libtcod.Color(255, 0, 0), EMPTY_CELL)
BLUE_BUILDING = BaseMapCell('', '#', libtcod.Color(0, 0, 255), BLOCK_CELL)
SAND = BaseMapCell('', '.', libtcod.Color(255, 255, 0), EMPTY_CELL)
BIKE = BaseMapCell('', 'b', libtcod.Color(50, 50, 250), BLOCK_CELL)
BLANK = BaseMapCell('', '_', libtcod.Color(255, 255, 255), BLOCK_CELL)
CAVE_ENTRANCE = BaseMapCell('', '>', libtcod.Color(200, 200, 200), BLOCK_CELL)
HEDGE = BaseMapCell('', '=', libtcod.Color(0, 255, 0), BLOCK_CELL)
LONG_GRASS = BaseMapCell('', ';', libtcod.Color(255, 255, 255), EMPTY_CELL)
DOOR = BaseMapCell('', '>', libtcod.Color(200, 200, 200), BLOCK_CELL)
ORANGE_BUILDING = BaseMapCell('', '#', libtcod.Color(200, 100, 0), BLOCK_CELL)
PINK_BUILDING = BaseMapCell('', '#', libtcod.Color(255, 100, 100), BLOCK_CELL)
YELLOW_BUILDING = BaseMapCell('', '#', libtcod.Color(200, 200, 0), BLOCK_CELL)
ROCK = BaseMapCell('', '^', libtcod.Color(70, 70, 70), BLOCK_CELL)
SIGN = BaseMapCell('', 's', libtcod.Color(200, 200, 200), BLOCK_CELL)
GREEN_BUILDING = BaseMapCell('', '#', libtcod.Color(0, 255, 0), BLOCK_CELL)
LEDGE = BaseMapCell('', '^', libtcod.Color(139, 69, 19), BLOCK_CELL)
GREY_BUILDING = BaseMapCell('', '#', libtcod.Color(100, 100, 100), BLOCK_CELL)
TREE = BaseMapCell('', '$', libtcod.Color(0, 255, 0), BLOCK_CELL)
WATER = BaseMapCell('', '.', libtcod.Color(0, 0, 255), WATER_CELL)
FENCE_VERTICAL = BaseMapCell('', 'X', libtcod.Color(139, 69, 19), BLOCK_CELL)
RED_BUILDING = BaseMapCell('', '#', libtcod.Color(200, 0, 0), BLOCK_CELL)