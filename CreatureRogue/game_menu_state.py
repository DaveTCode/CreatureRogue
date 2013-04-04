'''
    This is the state which represents the player being in the in game menu.
'''
import CreatureRogue.libtcodpy as libtcod

class InGameMenuState():
    '''
        The in game menu state is the main state that the game is in when the
        player is viewing a menu on the map.

        It uses two renderers (one to render the map and the other to render 
        the menu on top of it.)
    '''

    keys = [{"row": 1, "char": 'P', "str": "Pokedex"},
            {"row": 2, "char": 'A', "str": "Achievements"},
            {"row": -2, "char": 'S', "str": "Save"},
            {"row": -1, "char": 'Q', "str": "Quit"}]

    def __init__(self, game, game_data, map_renderer, menu_renderer):
        self.game = game
        self.game_data = game_data
        self.map_renderer = map_renderer
        self.menu_renderer = menu_renderer

    def handle_input(self, key):
        '''
            Handles input whilst in the menu state. Called once for each key up
            event whilst in this state.
        '''
        if key.vk == libtcod.KEY_ESCAPE:
            self.game.close_menu()
        elif key.vk == libtcod.KEY_CHAR and key.c == ord('q'):
            self.game.end_game()
        elif key.vk == libtcod.KEY_CHAR and key.c == ord('p'):
            self.game.load_pokedex()

    def render(self):
        '''
            Combine the map view and the menu view by blitting one onto the 
            other.
        '''
        console = self.map_renderer.render(self.game_data.player)

        sub_console = self.menu_renderer.render(InGameMenuState.keys)

        libtcod.console_blit(sub_console, 0, 0, 0, 0, console, libtcod.console_get_width(console) - libtcod.console_get_width(sub_console), 0)

        return console