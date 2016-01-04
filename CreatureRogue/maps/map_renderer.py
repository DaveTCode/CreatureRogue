"""
    Responsible for rendering a map of tiles onto the screen in ascii.
"""
from __future__ import division
import tcod as libtcod
import CreatureRogue.settings as settings


class MapCell:
    def __init__(self, base_cell):
        self.base_cell = base_cell

    def color(self):
        return self.base_cell.display_color

    def char(self):
        return self.base_cell.display_char


class BaseMapCell:
    def __init__(self, identifier, display_char, display_color, cell_passable_type):
        self.identifier = identifier
        self.display_char = display_char
        self.display_color = display_color
        self.cell_passable_type = cell_passable_type


class MapRenderer:
    def __init__(self, game):
        self.game = game
        self.console = libtcod.console.new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        self.start_x = self.start_y = 0

    def render(self, player):
        libtcod.console.clear(self.console)
        self._centre_map_on_player(player)
        self._render_map(player.map_data)
        self._render_player(player)

        return self.console

    def _centre_map_on_player(self, player):
        x, y = player.coords
        self.start_x = x - settings.SCREEN_WIDTH // 2
        self.start_y = y - settings.SCREEN_HEIGHT // 2

    def _render_player(self, player):
        x, y = player.coords

        libtcod.console.set_default_foreground(self.console, settings.PLAYER_COLOR)
        libtcod.console.put_char(self.console, x - self.start_x, y - self.start_y, '@')

    def _render_map(self, map):
        for y in range(self.start_y, self.start_y + settings.SCREEN_HEIGHT):
            for x in range(self.start_x, self.start_x + settings.SCREEN_WIDTH):
                if len(map.tiles) > y >= 0 and len(map.tiles[y]) > x >= 0:
                    cell = map.tiles[y][x]

                    libtcod.console.set_default_foreground(self.console, cell.color())
                    libtcod.console.put_char(self.console, x - self.start_x, y - self.start_y, cell.char())


# Passable cell types
BLOCK_CELL = 0
WATER_CELL = 1
EMPTY_CELL = 2

# Base cell types that maps can be made from
BRIDGE = BaseMapCell('bridge', '-', libtcod.Color(255, 255, 0), EMPTY_CELL)
STATUE = BaseMapCell('statue', 'S', libtcod.Color(70, 70, 70), BLOCK_CELL)
PATH = BaseMapCell('path', '-', libtcod.Color(255, 255, 255), EMPTY_CELL)
FENCE_HORIZONTAL = BaseMapCell('fence_horizontal', 'X', libtcod.Color(139, 69, 19), BLOCK_CELL)
GRASS = BaseMapCell('grass', '.', libtcod.Color(255, 255, 255), EMPTY_CELL)
LETTERBOX = BaseMapCell('letterbox', 'L', libtcod.Color(100, 100, 100), BLOCK_CELL)
FLOWER = BaseMapCell('flower', '.', libtcod.Color(255, 0, 0), EMPTY_CELL)
BLUE_BUILDING = BaseMapCell('blue_building', '#', libtcod.Color(0, 0, 255), BLOCK_CELL)
SAND = BaseMapCell('sand', '.', libtcod.Color(255, 255, 0), EMPTY_CELL)
BIKE = BaseMapCell('bike', 'b', libtcod.Color(50, 50, 250), BLOCK_CELL)
BLANK = BaseMapCell('blank', '_', libtcod.Color(255, 255, 255), BLOCK_CELL)
CAVE_ENTRANCE = BaseMapCell('cave_entrance', '>', libtcod.Color(200, 200, 200), BLOCK_CELL)
HEDGE = BaseMapCell('hedge', '=', libtcod.Color(0, 255, 0), BLOCK_CELL)
LONG_GRASS = BaseMapCell('long_grass', ';', libtcod.Color(255, 255, 255), EMPTY_CELL)
DOOR = BaseMapCell('door', '>', libtcod.Color(200, 200, 200), BLOCK_CELL)
ORANGE_BUILDING = BaseMapCell('orange_building', '#', libtcod.Color(200, 100, 0), BLOCK_CELL)
PINK_BUILDING = BaseMapCell('pink_building', '#', libtcod.Color(255, 100, 100), BLOCK_CELL)
YELLOW_BUILDING = BaseMapCell('yellow_building', '#', libtcod.Color(200, 200, 0), BLOCK_CELL)
ROCK = BaseMapCell('rock', '^', libtcod.Color(70, 70, 70), BLOCK_CELL)
SIGN = BaseMapCell('sign', 's', libtcod.Color(200, 200, 200), BLOCK_CELL)
GREEN_BUILDING = BaseMapCell('green_building', '#', libtcod.Color(0, 255, 0), BLOCK_CELL)
LEDGE = BaseMapCell('ledge', '^', libtcod.Color(139, 69, 19), BLOCK_CELL)
GREY_BUILDING = BaseMapCell('grey_building', '#', libtcod.Color(100, 100, 100), BLOCK_CELL)
TREE = BaseMapCell('tree', '$', libtcod.Color(0, 255, 0), BLOCK_CELL)
WATER = BaseMapCell('water', '.', libtcod.Color(0, 0, 255), WATER_CELL)
FENCE_VERTICAL = BaseMapCell('fence_vertical', 'X', libtcod.Color(139, 69, 19), BLOCK_CELL)
RED_BUILDING = BaseMapCell('red_building', '#', libtcod.Color(200, 0, 0), BLOCK_CELL)
