import libtcodpy as libtcod
import settings

TREE = 0
GRASS = 1
FLOWERS = 2
WATER = 3
WATER_BANK = 4
LONG_GRASS = 5
EXIT_NORTH = 6
EXIT_SOUTH = 7
EXIT_EAST = 8
EXIT_WEST = 9

class MapRenderer():

    type_char_map = {TREE: (libtcod.CHAR_SPADE, libtcod.green), GRASS: ('.', libtcod.white), WATER: ('.', libtcod.blue), WATER_BANK: (',', libtcod.blue), LONG_GRASS: (',', libtcod.white), EXIT_NORTH: ('^', libtcod.white), EXIT_SOUTH: ('^', libtcod.white), EXIT_WEST: ('<', libtcod.white), EXIT_EAST : ('>', libtcod.white)}
    
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
                char, color = MapRenderer.type_char_map[cell]
                
                libtcod.console_set_default_foreground(self.console, color)
                libtcod.console_put_char(self.console, x, y, char)