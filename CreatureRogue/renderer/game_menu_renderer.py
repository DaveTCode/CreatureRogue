"""
Responsible for rendering the main in game menu.
"""

import tcod

import CreatureRogue.settings as settings


class GameMenuRenderer:
    width = 30
    height = settings.SCREEN_HEIGHT

    def __init__(self, game):
        self.game = game
        self.console = tcod.console.Console(GameMenuRenderer.width, GameMenuRenderer.height)

    def render(self, keys):
        """
        Returns the completed menu console ready to be blitted onto another
        existing console.
        """
        self.console.clear()
        self.console.default_bg = settings.MENU_BG_COLOR

        self._render_lines()
        self._render_menu(keys)

        return self.console

    def _render_lines(self):
        self.console.draw_frame(
            0, 1, GameMenuRenderer.width - 1, GameMenuRenderer.height - 2
        )

    def _render_menu(self, keys):
        """
        Render the menu strings, these are passed in as dictionaries of the
        form:
        {row: <the row on which to place the menu item>,
         char: <the character which activates the menu item>,
         str: <The display string for the menu item>}

        If the row is negative it is taken as a reverse index from the
        bottom of the menu.
        """
        for key in keys:
            row = key["row"] + 1 if key["row"] >= 0 else GameMenuRenderer.height + key["row"] - 2
            self.console.print(2, row, "{}. {}".format(key["char"], key["str"]))
