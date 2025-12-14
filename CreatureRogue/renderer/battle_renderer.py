"""
Module contains all renderers which are used in battle
"""

from types import MappingProxyType

from tcod import libtcodpy
import tcod

import CreatureRogue.data_layer.data as data
import CreatureRogue.settings as settings
from CreatureRogue.data_layer.pokeball import Pokeball
from CreatureRogue.models.battle_data import BattleData
from CreatureRogue.models.creature import Creature


class CatchGraphicRenderer:
    """
    Independent renderer used to draw a pokeball onto the screen when
    attempting to catch a creature.
    """

    graphic = (
        (
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
            ("_", (0, 0, 0)),
            ("_", (0, 0, 0)),
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
        ),
        (
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
            ("/", (0, 0, 0)),
            ("_", (-2, -2, -2)),
            ("_", (-2, -2, -2)),
            ("\\", (0, 0, 0)),
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
        ),
        (
            (" ", (127, 127, 127)),
            ("/", (0, 0, 0)),
            ("_", (-2, -2, -2)),
            ("_", (-2, -2, -2)),
            ("_", (-2, -2, -2)),
            ("_", (-2, -2, -2)),
            ("\\", (0, 0, 0)),
            (" ", (127, 127, 127)),
        ),
        (
            ("|", (0, 0, 0)),
            ("_", (0, 0, 0)),
            ("_", (0, 0, 0)),
            ("/", (255, 255, 255)),
            ("\\", (255, 255, 255)),
            ("_", (0, 0, 0)),
            ("_", (0, 0, 0)),
            ("|", (0, 0, 0)),
        ),
        (
            ("|", (0, 0, 0)),
            ("_", (0, 0, 0)),
            ("_", (0, 0, 0)),
            ("\\", (255, 255, 255)),
            ("/", (255, 255, 255)),
            ("_", (0, 0, 0)),
            ("_", (0, 0, 0)),
            ("|", (0, 0, 0)),
        ),
        (
            (" ", (127, 127, 127)),
            ("\\", (0, 0, 0)),
            ("_", (-1, -1, -1)),
            ("_", (-1, -1, -1)),
            ("_", (-1, -1, -1)),
            ("_", (-1, -1, -1)),
            ("/", (0, 0, 0)),
            (" ", (127, 127, 127)),
        ),
        (
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
            ("\\", (0, 0, 0)),
            ("_", (-1, -1, -1)),
            ("_", (-1, -1, -1)),
            ("/", (0, 0, 0)),
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
        ),
        (
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
            ("_", (0, 0, 0)),
            ("_", (0, 0, 0)),
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
            (" ", (127, 127, 127)),
        ),
    )

    width = 30
    height = 20
    x_offset = (width - len(graphic[0])) // 2
    y_offset = (height - len(graphic)) // 2

    def __init__(self, game):
        self.game = game
        self.console = tcod.console.Console(
            CatchGraphicRenderer.width, CatchGraphicRenderer.height
        )

    def render(
        self, pokeball: Pokeball, percent_complete: float, message: str
    ) -> tcod.console.Console:
        """
        Render the area and return the full console
        """
        rows_complete = int(
            len(CatchGraphicRenderer.graphic) * (percent_complete / 100)
        )

        self.console.clear()
        self.console.default_bg = settings.CATCH_GRAPHIC_BG_COLOR
        self.console.default_fg = settings.LINE_COLOR
        self.console.draw_frame(
            0, 0, CatchGraphicRenderer.width, CatchGraphicRenderer.height
        )

        for y, row in enumerate(CatchGraphicRenderer.graphic):
            for x, cell in enumerate(row):
                if cell[0] != "":
                    if len(CatchGraphicRenderer.graphic) - y <= rows_complete:
                        if cell[1] == (-2, -2, -2):
                            color = pokeball.top_color
                        elif cell[1] == (-1, -1, -1):
                            color = pokeball.bottom_color
                        else:
                            color = cell[1]
                    else:
                        color = (127, 127, 127)

                    self.console.print(x + self.x_offset, y + self.y_offset, cell[0], fg=color)

        if message:
            self.console.print(
                CatchGraphicRenderer.width // 2,
                CatchGraphicRenderer.height - 3,
                message,
                width=CatchGraphicRenderer.width - 2,
                height=2,
                fg=settings.BATTLE_TEXT_COLOR,
                alignment=libtcodpy.CENTER,
            )

        return self.console


class LevelUpRenderer:
    """
    The level up renderer is used for rendering an overlay on top of the
    battle renderer indicating stat changes on level up.

    Whilst it's not technically an independent renderer it can still be
    used as one if required.
    """

    width = 35
    height = 13

    def __init__(self, game):
        self.game = game
        self.console = tcod.console.Console(
            LevelUpRenderer.width, LevelUpRenderer.height
        )

    def render(self, creature: Creature, prev_level: int) -> tcod.console.Console:
        """
        Returns a full console that can be blitted onto something else
        anywhere the calling code chooses.
        """
        self.console.clear()
        self.console.default_bg = settings.LEVEL_UP_BG_COLOR
        self._render_lines()
        self._render_summary(creature, prev_level)
        self._render_stats(creature, prev_level)

        return self.console

    def _render_lines(self):
        """
        Renders the border.
        """
        self.console.draw_frame(
            0, 0, LevelUpRenderer.width - 2, LevelUpRenderer.height - 2
        )

    def _render_summary(self, creature: Creature, prev_level: int):
        """
        Render the summary line at the top of the console.
        """
        summary_str = f"Level {prev_level} -> {creature.level}"
        self.console.print(5, 3, summary_str, fg=settings.BATTLE_TEXT_COLOR)

    def _render_stats(self, creature: Creature, prev_level: int):
        """
        Render the statistics lines one by one.
        """
        for idx, stat in enumerate(
            [
                stat
                for stat in creature.stats
                if stat.short_name is not None and stat.short_name != ""
            ]
        ):
            stat_str = f"{stat.short_name:7s}: {creature.max_stat(stat, level=prev_level):3d} -> {creature.max_stat(stat):3d}"

            self.console.print(5, 4 + idx, stat_str, fg=settings.BATTLE_TEXT_COLOR)


class BattleRenderer:
    """
    The battle renderer is used to display a battle on the screen.

    It returns a console which is sized at the entire of the screen.
    """

    options = (
        MappingProxyType({"row": -2, "char": "C", "desc": "Capture"}),
        MappingProxyType({"row": -1, "char": "F", "desc": "Flee"}),
    )
    bottom_section_height = 16
    top_section_height = settings.SCREEN_HEIGHT - bottom_section_height
    option_area_width = 40
    message_area_width = settings.SCREEN_WIDTH - option_area_width
    message_height = 12
    left_padding = 2
    top_padding = 2

    creature_details_width = 30
    creature_details_height_w_hp = 8
    creature_details_height_no_hp = 6

    defending_creature_x = 2
    defending_creature_y = 4
    attacking_creature_x = settings.SCREEN_WIDTH - creature_details_width - 2
    attacking_creature_y = top_section_height - creature_details_height_w_hp - 4

    def __init__(self, game):
        self.game = game
        self.console = tcod.console.Console(
            settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        )

    def render(
        self, battle_data: BattleData, messages: list[str], selecting_pokeball: bool
    ) -> tcod.console.Console:
        """
        The external interface to this class. Call this to render the
        given battle data object.
        """
        self.console.clear(fg=settings.FOREGROUND_COLOR, bg=settings.BACKGROUND_COLOR)
        self._render_lines()

        self._render_creature_details(
            battle_data.defending_creature().creature,
            BattleRenderer.defending_creature_x,
            BattleRenderer.defending_creature_y,
            include_health_values=False,
        )
        self._render_creature_details(
            battle_data.player_creature.creature,
            BattleRenderer.attacking_creature_x,
            BattleRenderer.attacking_creature_y,
            include_health_values=True,
        )

        if selecting_pokeball:
            self._render_pokeball_select(
                self.game.game_data.player.available_pokeballs(),
                x=BattleRenderer.left_padding,
                y=BattleRenderer.top_section_height + 2,
            )
        else:
            self._render_options(
                battle_data.player_creature.creature,
                x=BattleRenderer.left_padding,
                y=BattleRenderer.top_section_height + 2,
            )

            self._render_blank_message_box(
                x=BattleRenderer.option_area_width,
                y=BattleRenderer.top_section_height,
                width=BattleRenderer.message_area_width,
                height=BattleRenderer.bottom_section_height,
            )
            if len(messages):
                self._render_message(
                    message=messages[0],
                    x=BattleRenderer.option_area_width,
                    y=BattleRenderer.top_section_height + 4,
                )

        return self.console

    def _render_lines(self):
        """
        Renders the lines which separate sections of the screen.
        """
        self.console.draw_rect(
            0,
            BattleRenderer.top_section_height,
            settings.SCREEN_WIDTH,
            1,
            ch=ord("-"),
            fg=settings.LINE_COLOR,
        )

    def _render_creature_details(
        self, creature: Creature, x: int, y: int, include_health_values: bool = False
    ):
        """
        Renders the creature box for the defending creature.
        """
        height = (
            BattleRenderer.creature_details_height_w_hp
            if include_health_values
            else BattleRenderer.creature_details_height_no_hp
        )

        self.console.draw_frame(
            x,
            y,
            BattleRenderer.creature_details_width,
            height,
            fg=settings.BATTLE_TEXT_COLOR,
        )
        self.console.print(
            x + 1, y + 1, creature.nickname[:10], fg=settings.BATTLE_TEXT_COLOR
        )
        self.console.print(
            x + BattleRenderer.creature_details_width - 6,
            y + 1,
            f"LV.{creature.level}",
            fg=settings.BATTLE_TEXT_COLOR,
        )

        self._render_health_bar(
            creature, BattleRenderer.creature_details_width - 2, x + 1, y + 3
        )
        if include_health_values:
            self._render_health_values(
                creature, x + BattleRenderer.creature_details_width - 8, y + 5
            )

    def _render_health_bar(self, creature: Creature, max_length: int, x: int, y: int):
        """
        Utility function to render a health bar for the given creature at
        the given x and y coordinates.
        """
        hp_stat = self.game.static_game_data.stat(data.HP_STAT)
        health_bars = int(
            (creature.current_stat(hp_stat) / creature.max_stat(hp_stat)) * max_length
        )

        if health_bars > max_length / 2:
            color = settings.GOOD_HEALTH_COLOR
        elif health_bars > max_length / 4:
            color = settings.HALF_HEALTH_COLOR
        else:
            color = settings.LOW_HEALTH_COLOR

        for i in range(x, x + health_bars):
            self.console.print(i, y, "=", fg=color)

        for i in range(x + health_bars, x + max_length):
            self.console.print(i, y, "=", fg=settings.BLANK_HEALTH_COLOR)

    def _render_health_values(self, creature: Creature, x: int, y: int):
        """
        Utility function to render the health values <current>/<max> at
        the given x,y coordinates.
        """
        hp_stat = self.game.static_game_data.stat(data.HP_STAT)
        current = creature.current_stat(hp_stat)
        max_hp = creature.max_stat(hp_stat)

        self.console.print(x, y, f"{current}/{max_hp}", fg=settings.BATTLE_TEXT_COLOR)

    def _render_options(self, creature: Creature, x: int, y: int):
        """
        Renders all moves and additional options such as "Flee", "Capture".

        These are defined in the class level variable "options"
        """
        for row, move in enumerate(creature.moves):
            self.console.print(
                x,
                y + row,
                f"{row + 1}. {move.move_data.name:15s}{move.move_data.type.name:>12s}  {move.pp}/{move.move_data.max_pp}",
            )

        for option in BattleRenderer.options:
            display = True

            # Special case code for capture, disable it if the player has no
            # pokeballs remaining. Probably generalise when obvious what other
            # options there will be.
            if (
                option["desc"] == "Capture"
                and len(self.game.game_data.player.available_pokeballs()) <= 0
            ):
                display = False

            if display:
                actual_row = settings.SCREEN_HEIGHT + int(option["row"]) - 1
                self.console.print(
                    x,
                    actual_row,
                    "{}. {}".format(option["char"], option["desc"]),
                )

    def _render_blank_message_box(self, x: int, y: int, width: int, height: int):
        """
        Utility function to render the box in which messages go.
        """
        self.console.draw_frame(x, y, width, height)

    def _render_message(self, message: str, x: int, y: int):
        """
        Utility function to render a message on top of the screen at the
        given point.
        """
        self.console.print(x + 1, y + 1, message)

    def _render_pokeball_select(self, pokeballs: dict[Pokeball, int], x: int, y: int):
        """
        Render the list of available pokeball types along with the key
        press required to select them.
        """
        for row, pokeball in enumerate(pokeballs.keys()):
            self.console.print(
                x,
                y + row + 1,
                "{}. {:20s}{}".format(
                    pokeball.display_char, pokeball.name + " Ball", pokeballs[pokeball]
                ),
            )
