"""
The main game state when the player is viewing the pokedex.

Handles input and rendering and allows the player to return to the main
game state.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from CreatureRogue.game import Game
    from CreatureRogue.models.game_data import GameData
    from CreatureRogue.renderer.pokedex_renderer import PokedexRenderer

import tcod


class PokedexState:
    def __init__(self, game: "Game", game_data: "GameData", pokedex_renderer: "PokedexRenderer"):
        self.game = game
        self.game_data = game_data
        self.pokedex_renderer = pokedex_renderer

        self.selected_column = 0
        self.selected_row = 0
        self.viewing_species = None
        self.left_most_column = 0

    def displaying_species(self):
        """
        Returns True if the species details box is displayed otherwise
        false.
        """
        return self.viewing_species is not None

    def display_selected(self):
        """
        Display the currently selected species (as specified by
        self.selected_row, self.selected_column).
        """
        pokedex_id = self.pokedex_renderer.calculate_pokedex_number_of_position(
            self.selected_column, self.selected_row
        )

        if (
            len(self.game_data.player.pokedex) > pokedex_id
            and self.game_data.player.pokedex[pokedex_id][0] > 0
        ):
            self.viewing_species = pokedex_id

    def close_display(self):
        """
        External interface to indicate that we are to stop viewing the
        current species.
        """
        self.viewing_species = None

    def shift_row(self, delta):
        """
        Changes which row is currently selected. Bounds the row by the
        maximum number so that the row index is never out of the
        valid range.
        """
        self.selected_row = self.selected_row + delta
        if self.selected_row < 0:
            self.selected_row = 0
        elif self.selected_row > self.pokedex_renderer.max_rows:
            self.selected_row = self.pokedex_renderer.max_rows

    def shift_column(self, delta):
        """
        Changes which column is currently selected. Bounds the column by
        the maximum number so that the row index is never out of the
        valid range.
        """
        self.selected_column = self.selected_column + delta
        if self.selected_column < 0:
            self.selected_column = 0
        elif self.selected_column > self.pokedex_renderer.max_columns:
            self.selected_column = self.pokedex_renderer.max_columns

        while self.selected_column - self.left_most_column >= 4:
            self.left_most_column += 1
        while self.selected_column < self.left_most_column:
            self.left_most_column -= 1

    def handle_input(self, event: tcod.event.KeyDown):
        """
        Handles a single key press when viewing the pokedex.
        """
        if self.displaying_species():
            if event.sym == tcod.event.KeySym.ESCAPE:
                self.close_display()
        else:
            if event.sym == tcod.event.KeySym.LEFT:
                self.shift_column(-1)
            elif event.sym == tcod.event.KeySym.RIGHT:
                self.shift_column(1)
            elif event.sym == tcod.event.KeySym.UP:
                self.shift_row(-1)
            elif event.sym == tcod.event.KeySym.DOWN:
                self.shift_row(1)
            elif event.sym == tcod.event.KeySym.RETURN:
                self.display_selected()
            elif event.sym == tcod.event.KeySym.ESCAPE:
                self.game.close_pokedex()

    def render(self) -> tcod.console.Console:
        """
        Passes control off to the pokedex renderer to display the current
        pokedex state.
        """
        return self.pokedex_renderer.render(
            self.game_data.player.pokedex,
            self.viewing_species,
            self.selected_row,
            self.selected_column,
            self.left_most_column,
        )
