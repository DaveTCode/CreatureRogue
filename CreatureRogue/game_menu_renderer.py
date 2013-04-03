'''
    Responsible for rendering the main in game menu.
'''
import CreatureRogue.libtcodpy as libtcod
import CreatureRogue.settings as settings

class GameMenuRenderer():
    
    width = 40
    height = settings.SCREEN_HEIGHT

    def __init__(self, game):
        self.game = game
        self.console = libtcod.console_new(GameMenuRenderer.width, GameMenuRenderer.height)
        
    def render(self, keys):
        '''
            Returns the completed menu console ready to be blitted onto another
            existing console.
        '''
        libtcod.console_clear(self.console)
        libtcod.console_set_default_background(self.console, settings.MENU_BG_COLOR)

        self._render_lines()
        self._render_menu(keys)

        return self.console

    def _render_lines(self):
        libtcod.console_print_frame(self.console, 0, 1, GameMenuRenderer.width - 1, GameMenuRenderer.height - 2)

    def _render_menu(self, keys):
        '''
            Render the menu strings, these are passed in as dictionaries of the 
            form:
            {row: <the row on which to place the menu item>,
             char: <the character which activates the menu item>,
             str: <The display string for the menu item>}

            If the row is negative it is taken as a reverse index from the 
            bottom of the menu.
        '''
        for key in keys:
            row = key["row"] + 1 if key["row"] >= 0 else GameMenuRenderer.height + key["row"] - 2
            libtcod.console_print(self.console, 2, row, "{0}. {1}".format(key["char"], key["str"]))