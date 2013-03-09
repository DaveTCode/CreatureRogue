import libtcodpy as libtcod
import settings

class MapCell():

    def __init__(self, base_cell, exit_location = None):
        self.base_cell = base_cell
        self.exit_location = exit_location
    
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
    
    def __init__(self, console):
        self.console = console
        
    def render(self, player):
        self._render_map(player.map, 0, 0)
        self._render_player(player, 0, 0)
        
    def _render_player(self, player, x_start, y_start):
        x,y = player.coords
    
        libtcod.console_set_default_foreground(self.console, settings.PLAYER_COLOR)
        libtcod.console_put_char(self.console, x + x_start, y + y_start, '@')
    
    def _render_map(self, map, x_start, y_start):
        for y in range(y_start, y_start + len(map.tiles)):
            row = map.tiles[y - y_start]
            for x in range(x_start, x_start + len(row)):
                cell = row[x - x_start]
                
                libtcod.console_set_default_foreground(self.console, cell.color())
                libtcod.console_put_char(self.console, x, y, cell.char())

# Passable cell types
BLOCK_CELL = 0
WATER_CELL = 1
EMPTY_CELL = 2

# Base cell types that maps can be made from
TREE = BaseMapCell('tree', libtcod.CHAR_SPADE, libtcod.green, BLOCK_CELL)
GRASS = BaseMapCell('grass', '.', libtcod.white, EMPTY_CELL)
WATER = BaseMapCell('water', '.', libtcod.blue, WATER_CELL)
WATER_BANK = BaseMapCell('waterbank', ',', libtcod.blue, WATER_CELL)
LONG_GRASS = BaseMapCell('longgrass', ';', libtcod.white, EMPTY_CELL)
EXIT_NORTH = BaseMapCell('exitnorth', '^', libtcod.white, EMPTY_CELL)
EXIT_SOUTH = BaseMapCell('exitsouth', '^', libtcod.white, EMPTY_CELL)
EXIT_EAST = BaseMapCell('exiteast', '>', libtcod.white, EMPTY_CELL)
EXIT_WEST = BaseMapCell('exitwest', '<', libtcod.white, EMPTY_CELL)
WATER_EXIT_NORTH = BaseMapCell('exitnorth', '^', libtcod.blue, WATER_CELL)
WATER_EXIT_SOUTH = BaseMapCell('exitsouth', '^', libtcod.blue, WATER_CELL)
WATER_EXIT_EAST = BaseMapCell('exiteast', '>', libtcod.blue, WATER_CELL)
WATER_EXIT_WEST = BaseMapCell('exitwest', '<', libtcod.blue, WATER_CELL)