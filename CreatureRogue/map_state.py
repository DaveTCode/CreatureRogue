"""
    The map state is the state that is used when the player is traversing the
    world map.

    All states are responsible for rendering and input handling.
"""

import tcod as libtcod


class MapState:

    def __init__(self, game, game_data, map_renderer):
        self.game = game
        self.game_data = game_data
        self.map_renderer = map_renderer
        self.top_left = 0
        self.top_right = 0

    def handle_input(self, key):
        """
            Handles a single key stroke when the player is traversing the map.
        """
        x_delta, y_delta = 0, 0
        if key.vk == libtcod.KEY_ESCAPE:
            self.game.open_menu()
        elif key.vk == libtcod.KEY_LEFT:
            x_delta = -1
        elif key.vk == libtcod.KEY_RIGHT:
            x_delta = 1
        elif key.vk == libtcod.KEY_UP:
            y_delta = -1
        elif key.vk == libtcod.KEY_DOWN:
            y_delta = 1
        
        if x_delta != 0 or y_delta != 0:
            new_y, new_x = y_delta + self.game_data.player.coords[1], x_delta + self.game_data.player.coords[0]
            
            try:
                next_cell = self.game_data.player.map_data.tiles[new_y][new_x]
                
                moved, caused_wild_encounter = self.game_data.player.move_to_cell(new_x, new_y)

                if caused_wild_encounter:
                    self.game.start_wild_battle()
            except KeyError:
                pass

    def render(self):
        """
            Handles rendering whilst in this state
        """
        return self.map_renderer.render(self.game_data.player)
