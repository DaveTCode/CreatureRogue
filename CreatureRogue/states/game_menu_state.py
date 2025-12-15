"""
This is the state which represents the player being in the in game menu.
"""

from types import MappingProxyType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

import tcod


class InGameMenuState:
    """
    The in game menu state is the main state that the game is in when the
    player is viewing a menu on the map.

    It uses two renderers (one to render the map and the other to render
    the menu on top of it.)
    """

    keys = (
        MappingProxyType({"row": 1, "char": "P", "str": "Pokedex"}),
        MappingProxyType({"row": 2, "char": "A", "str": "Achievements"}),
        MappingProxyType({"row": -2, "char": "S", "str": "Save"}),
        MappingProxyType({"row": -1, "char": "Q", "str": "Quit"}),
    )

    def __init__(
        self,
        game,  # type: Game
        game_data,  # type: GameData
        map_renderer,  # type: MapRenderer
        menu_renderer,  # type: GameMenuRenderer
    ):
        self.game = game
        self.game_data = game_data
        self.map_renderer = map_renderer
        self.menu_renderer = menu_renderer

    def handle_input(self, event: tcod.event.KeyDown):
        """
        Handles input whilst in the menu state. Called once for each key up
        event whilst in this state.
        """
        if event.sym == tcod.event.KeyEscape:
            self.game.close_menu()
        elif event.sym == ord("q"):
            self.game.end_game()
        elif event.sym == ord("p"):
            self.game.load_pokedex()

    def render(self):
        """
        Combine the map view and the menu view by blitting one onto the
        other.
        """
        console = self.map_renderer.render(self.game_data.player)

        sub_console = self.menu_renderer.render(InGameMenuState.keys)
        sub_console.blit(console, console.width - sub_console.width, 0, 0, 0, 0, 0)

        return console
