"""
Handles rendering jobs when the game is in the "View pokedex" state.
"""

import tcod

from CreatureRogue.data_layer.species import Species
import CreatureRogue.settings as settings


class PokedexRenderer:
    header_height = 5
    column_width = settings.SCREEN_WIDTH // 4
    column_height = settings.SCREEN_HEIGHT - header_height - 2
    width = settings.SCREEN_WIDTH

    def __init__(self, game):
        self.game = game
        self.console = tcod.console.Console(
            settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        )

        self.max_rows = self.column_height - 1
        self.max_columns = len(self.game.static_game_data.species) // self.column_height

    def render(
        self, pokedex, viewing_species, selected_row, selected_column, left_most_column
    ):
        """
        Major external interface to this class.

        Renders the entire of the pokedex passed in to the console which
        was originally set on the class. Doesn't blit back onto the main
        console as this is the job of the caller.
        """
        self.console.clear()
        self._render_lines()

        self._render_selection(selected_row, selected_column, left_most_column)

        self._render_species(pokedex, left_most_column)

        if viewing_species:
            status, species = pokedex[viewing_species]

            if status > 0:
                self._render_details_box(species, status)

        return self.console

    def _render_lines(self):
        """
        Render the lines which make up the structure of the pokedex.
        """
        self.console.draw_rect(
            0,
            PokedexRenderer.header_height,
            PokedexRenderer.width,
            1,
            ch=ord("-"),
            fg=settings.POKEDEX_LINE_COLOR,
        )
        for i in range(
            PokedexRenderer.column_width,
            PokedexRenderer.width,
            PokedexRenderer.column_width,
        ):
            self.console.draw_rect(
                i,
                PokedexRenderer.header_height,
                1,
                PokedexRenderer.column_height,
                ch=ord("|"),
                fg=settings.POKEDEX_LINE_COLOR,
            )

    def _render_selection(self, selected_row, selected_column, left_most_column):
        """
        Render the information on which row, column is currently selected.
        """
        self.console.default_fg = settings.POKEDEX_LINE_COLOR
        self.console.print(
            (selected_column - left_most_column) * PokedexRenderer.column_width + 19,
            selected_row + PokedexRenderer.header_height + 1,
            "<",
            fg=settings.POKEDEX_LINE_COLOR,
        )

    def _render_species(self, pokedex, left_most_column):
        """
        Iterate over all species and put them onto the screen in the
        appropriate location.

        Only displays seen and known species. Each of these can be
        displayed differently.
        """
        for pokedex_number in pokedex:
            status, species = pokedex[pokedex_number]

            name = "???"
            color = settings.POKEDEX_UNKNOWN_COLOR
            if status == 1:
                name = species.name
                color = settings.POKEDEX_SEEN_COLOR
            elif status == 2:
                name = species.name
                color = settings.POKEDEX_KNOWN_COLOR

            column, row = self.calculate_position_of_pokedex_number(
                pokedex_number - 1, left_most_column
            )

            self.console.print(
                column * PokedexRenderer.column_width + 1,
                row + PokedexRenderer.header_height + 1,
                str(pokedex_number) + ". " + name,
                fg=color,
            )

    def _render_details_box(self, species: Species, status: int):
        """
        If a pokemon has been selected then this is called to display a
        box with the specific details as an overlay on top of the pokedex.
        """
        self.console.draw_frame(
            19, 15, 43, 16, fg=settings.POKEDEX_LINE_COLOR
        )  # TODO: Generalise to widths

        self.console.print(
            23,
            16,
            f"No. {species.pokedex_number:0=3d}  {species.name}",
            fg=settings.POKEDEX_LINE_COLOR,
        )

        if status == 2:
            self.console.print(
                23, 17, f"  {species.genus} Pokemon", fg=settings.POKEDEX_LINE_COLOR
            )
            self.console.print(
                23,
                18,
                "Type(s): {}".format(
                    ", ".join(str(t) for t in species.types),
                ),
                fg=settings.POKEDEX_LINE_COLOR,
            )
            self.console.print(
                23,
                19,
                f"Height: {species.imperial_height_str()}",
                fg=settings.POKEDEX_LINE_COLOR,
            )
            self.console.print(
                23,
                20,
                f"Weight: {species.imperial_weight_str()}",
                fg=settings.POKEDEX_LINE_COLOR,
            )

            self.console.print(
                20, 22, species.flavor_text, fg=settings.POKEDEX_LINE_COLOR
            )
        elif status == 1:
            self.console.print(
                23, 17, "  ????? Pokemon", fg=settings.POKEDEX_LINE_COLOR
            )
            self.console.print(23, 18, "Type(s): ?????", fg=settings.POKEDEX_LINE_COLOR)
            self.console.print(
                23, 19, "Height: ??'??\"", fg=settings.POKEDEX_LINE_COLOR
            )
            self.console.print(
                23, 20, "Weight: ????.? lbs.", fg=settings.POKEDEX_LINE_COLOR
            )

    @staticmethod
    def calculate_position_of_pokedex_number(
        pokedex_number: int, left_most_column: int
    ):
        """
        Given a number in the pokedex this backtracks to find the x, y
        coordinates in the output.

        :param pokedex_number:
        :param left_most_column:
        """
        return (
            pokedex_number // PokedexRenderer.column_height - left_most_column,
            pokedex_number % PokedexRenderer.column_height,
        )

    @staticmethod
    def calculate_pokedex_number_of_position(column: int, row: int):
        """
        Given x, y coordinates in the output table this returns the
        pokedex number of the creature to be found there.

        :param row:
        :param column:
        """
        return column * PokedexRenderer.column_height + row + 1
