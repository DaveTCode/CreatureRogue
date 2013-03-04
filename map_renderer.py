from maps import *
import libtcodpy as libtcod

TREE = 0
GRASS = 1
FLOWERS = 2
WATER = 3
WATER_BANK = 4
SIGN = 5

class MapRenderer():

    type_char_map = {TREE: 157, }
    
    def __init__(self, console):
        self.console = console
        
    def render(self, map):
        self._render_map(map, 0, 0)
    
    def _render_map(self, map, x_start, y_start):
        for y in range(y_start, y_start + len(map.tiles)):
            row = map[y - y_start]
            for x in range(x_start, x_start + len(row)):
                cell = row[x - x_start]
                
                libtcod.console_put_char(self.console, x, y, type_char_map[cell])