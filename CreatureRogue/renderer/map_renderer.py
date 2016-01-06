"""
    Responsible for rendering a map of tiles onto the screen in ascii.
"""
import tcod as libtcod

import CreatureRogue.settings as settings
from CreatureRogue.data_layer.map_loader import MapData


class MapRenderer:
    def __init__(self):
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

    def _render_map(self, map_data: MapData):
        for y in range(self.start_y, self.start_y + settings.SCREEN_HEIGHT):
            for x in range(self.start_x, self.start_x + settings.SCREEN_WIDTH):
                if len(map_data.tiles) > y >= 0 and len(map_data.tiles[y]) > x >= 0:
                    cell = map_data.tiles[y][x]

                    libtcod.console.set_default_foreground(self.console, cell.color)
                    libtcod.console.put_char(self.console, x - self.start_x, y - self.start_y, cell.display_character)
