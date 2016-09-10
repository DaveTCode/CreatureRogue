"""
    Module contains all renderers which are used in battle
"""
import tcod as libtcod
from typing import Dict, List

from CreatureRogue.game import Game
import CreatureRogue.data_layer.data as data
from CreatureRogue.data_layer.pokeball import Pokeball
from CreatureRogue.models.battle_data import BattleData
from CreatureRogue.models.creature import Creature
import CreatureRogue.settings as settings


class CatchGraphicRenderer:
    """
        Independent renderer used to draw a pokeball onto the screen when 
        attempting to catch a creature.
    """
    graphic = [[(' ', libtcod.gray), (' ', libtcod.gray), (' ', libtcod.gray), ('_', libtcod.black), ('_', libtcod.black), (' ', libtcod.gray), (' ', libtcod.gray), (' ', libtcod.gray)],
               [(' ', libtcod.gray), (' ', libtcod.gray), ('/', libtcod.black), ('_', "upper"), ('_', "upper"), ('\\', libtcod.black), (' ', libtcod.gray), (' ', libtcod.gray)],
               [(' ', libtcod.gray), ('/', libtcod.black), ('_', "upper"), ('_', "upper"), ('_', "upper"), ('_', "upper"), ('\\', libtcod.black), (' ', libtcod.gray)],
               [('|', libtcod.black), ('_', libtcod.black), ('_', libtcod.black), ('/', libtcod.white), ('\\', libtcod.white), ('_', libtcod.black), ('_', libtcod.black), ('|', libtcod.black)],
               [('|', libtcod.black), ('_', libtcod.black), ('_', libtcod.black), ('\\', libtcod.white), ('/', libtcod.white), ('_', libtcod.black), ('_', libtcod.black), ('|', libtcod.black)],
               [(' ', libtcod.gray), ('\\', libtcod.black), ('_', "lower"), ('_', "lower"), ('_', "lower"), ('_', "lower"), ('/', libtcod.black), (' ', libtcod.gray)],
               [(' ', libtcod.gray), (' ', libtcod.gray), ('\\', libtcod.black), ('_', "lower"), ('_', "lower"), ('/', libtcod.black), (' ', libtcod.gray), (' ', libtcod.gray)],
               [(' ', libtcod.gray), (' ', libtcod.gray), (' ', libtcod.gray), ('_', libtcod.black), ('_', libtcod.black), (' ', libtcod.gray), (' ', libtcod.gray), (' ', libtcod.gray)]]

    width = 30
    height = 20
    x_offset = (width - len(graphic[0])) // 2
    y_offset = (height - len(graphic)) // 2

    def __init__(self, game: Game):
        self.game = game
        self.console = libtcod.console.new(CatchGraphicRenderer.width, CatchGraphicRenderer.height)

    def render(self, pokeball: Pokeball, percent_complete: float, message: str) -> libtcod.console:
        """
            Render the area and return the full console
        """
        rows_complete = int(len(CatchGraphicRenderer.graphic) * (percent_complete / 100))

        libtcod.console.clear(self.console)
        libtcod.console.set_default_background(self.console, settings.CATCH_GRAPHIC_BG_COLOR)
        libtcod.console.set_default_foreground(self.console, settings.LINE_COLOR)
        libtcod.console.print_frame(self.console, 0, 0, CatchGraphicRenderer.width, CatchGraphicRenderer.height)

        for y, row in enumerate(CatchGraphicRenderer.graphic):
            for x, cell in enumerate(row):
                if cell[0] != '':
                    if len(CatchGraphicRenderer.graphic) - y <= rows_complete:
                        if cell[1] == "upper":
                            color = pokeball.top_color
                        elif cell[1] == "lower":
                            color = pokeball.bottom_color
                        else:
                            color = cell[1]
                    else:
                        color = libtcod.gray

                    libtcod.console.set_default_foreground(self.console, color)
                    libtcod.console.put_char(self.console, x + self.x_offset, y + self.y_offset, cell[0])

        if message:
            libtcod.console.print_rect_ex(self.console,
                                          CatchGraphicRenderer.width // 2, CatchGraphicRenderer.height - 3, 
                                          CatchGraphicRenderer.width - 2, 2, 
                                          libtcod.BKGND_NONE, libtcod.CENTER, message)

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
    
    def __init__(self, game: Game):
        self.game = game
        self.console = libtcod.console.new(LevelUpRenderer.width, LevelUpRenderer.height)

    def render(self, creature: Creature, prev_level: int) -> libtcod.console:
        """
            Returns a full console that can be blitted onto something else
            anywhere the calling code chooses.
        """
        libtcod.console.clear(self.console)
        libtcod.console.set_default_background(self.console, settings.LEVEL_UP_BG_COLOR)
        self._render_lines()
        self._render_summary(creature, prev_level)
        self._render_stats(creature, prev_level)

        return self.console

    def _render_lines(self):
        """
            Renders the border.
        """
        libtcod.console.print_frame(self.console, 1, 1, LevelUpRenderer.width - 2, LevelUpRenderer.height - 2)

    def _render_summary(self, creature: Creature, prev_level: int):
        """
            Render the summary line at the top of the console.
        """
        summary_str = "Level {0} -> {1}".format(prev_level, creature.level)
        libtcod.console.set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console.print(self.console, 5, 3, summary_str)

    def _render_stats(self, creature: Creature, prev_level: int):
        """
            Render the statistics lines one by one.
        """
        libtcod.console.set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)

        for idx, stat in enumerate([stat for stat in creature.stats if stat.short_name is not None and stat.short_name != ""]):
            stat_str = "{0:7s}: {1:3d} -> {2:3d}".format(stat.short_name, creature.max_stat(stat, level=prev_level), creature.max_stat(stat))

            libtcod.console.print(self.console, 5, 4 + idx, stat_str)


class BattleRenderer:
    """
        The battle renderer is used to display a battle on the screen.
        
        It returns a console which is sized at the entire of the screen.
    """

    options = [{"row": -2, "char": "C", "desc": "Capture"},
               {"row": -1, "char": "F", "desc": "Flee"}]
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

    def __init__(self, game: Game):
        self.game = game
        self.console = libtcod.console.new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        
    def render(self, battle_data: BattleData, messages: List[str], selecting_pokeball: bool) -> libtcod.console:
        """
            The external interface to this class. Call this to render the
            given battle data object.
        """
        libtcod.console.clear(self.console)
        self._render_lines()
        
        self._render_creature_details(battle_data.defending_creature().creature, 
                                      BattleRenderer.defending_creature_x, 
                                      BattleRenderer.defending_creature_y, 
                                      include_health_values=False)
        self._render_creature_details(battle_data.player_creature.creature, 
                                      BattleRenderer.attacking_creature_x, 
                                      BattleRenderer.attacking_creature_y, 
                                      include_health_values=True)
        
        if selecting_pokeball:
            self._render_pokeball_select(self.game.game_data.player.available_pokeballs(),
                                         x=BattleRenderer.left_padding, 
                                         y=BattleRenderer.top_section_height + 2)
        else:
            self._render_options(battle_data.player_creature.creature, 
                                 x=BattleRenderer.left_padding, 
                                 y=BattleRenderer.top_section_height + 2)
            
            self._render_blank_message_box(x=BattleRenderer.option_area_width, 
                                           y=BattleRenderer.top_section_height, 
                                           width=BattleRenderer.message_area_width, 
                                           height=BattleRenderer.bottom_section_height)
            if len(messages):
                self._render_message(message=messages[0], 
                                     x=BattleRenderer.option_area_width, 
                                     y=BattleRenderer.top_section_height + 4)

        return self.console
        
    def _render_lines(self):
        """
            Renders the lines which separate sections of the screen.
        """
        libtcod.console.set_default_foreground(self.console, settings.LINE_COLOR)
        libtcod.console.hline(self.console, 0, BattleRenderer.top_section_height, settings.SCREEN_WIDTH)

    def _render_creature_details(self, creature: Creature, x: int, y: int, include_health_values: bool=False):
        """
            Renders the creature box for the defending creature.
        """
        height = BattleRenderer.creature_details_height_w_hp if include_health_values else BattleRenderer.creature_details_height_no_hp

        libtcod.console.set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console.print_frame(self.console, x, y, BattleRenderer.creature_details_width, height)
        libtcod.console.print(self.console, x + 1, y + 1, creature.nickname[:10])
        libtcod.console.print(self.console, x + BattleRenderer.creature_details_width - 6, y + 1, "LV.{0}".format(creature.level))
        
        self._render_health_bar(creature, BattleRenderer.creature_details_width - 2, x + 1, y + 3)
        if include_health_values:
            self._render_health_values(creature, x + BattleRenderer.creature_details_width - 8, y + 5)
            
    def _render_health_bar(self, creature: Creature, max_length: int, x: int, y: int):
        """
            Utility function to render a health bar for the given creature at
            the given x and y coordinates.
        """
        hp_stat = self.game.static_game_data.stat(data.HP_STAT)
        health_bars = int((creature.current_stat(hp_stat) / creature.max_stat(hp_stat)) * max_length)
        
        if health_bars > max_length / 2:
            color = settings.GOOD_HEALTH_COLOR
        elif health_bars > max_length / 4:
            color = settings.HALF_HEALTH_COLOR
        else:
            color = settings.LOW_HEALTH_COLOR
            
        libtcod.console.set_default_foreground(self.console, color)
        for i in range(x, x + health_bars):
            libtcod.console.put_char(self.console, i, y, '=')
            
        libtcod.console.set_default_foreground(self.console, settings.BLANK_HEALTH_COLOR)
        for i in range(x + health_bars, x + max_length):
            libtcod.console.put_char(self.console, i, y, '=')
            
    def _render_health_values(self, creature: Creature, x: int, y: int):
        """
            Utility function to render the health values <current>/<max> at 
            the given x,y coordinates.
        """
        hp_stat = self.game.static_game_data.stat(data.HP_STAT)
        current = creature.current_stat(hp_stat)
        max_hp = creature.max_stat(hp_stat)
        
        libtcod.console.set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console.print(self.console, x, y, "{0}/{1}".format(current, max_hp))

    def _render_options(self, creature: Creature, x: int, y: int):
        """
            Renders all moves and additional options such as "Flee", "Capture".

            These are defined in the class level variable "options"
        """
        for row, move in enumerate(creature.moves):
            libtcod.console.print(self.console, x, y + row,
                                  "{0}. {1:15s}{2:>12s}  {3}/{4}".format(row + 1, 
                                                                         move.move_data.name, 
                                                                         move.move_data.type.name, 
                                                                         move.pp, 
                                                                         move.move_data.max_pp))

        for option in BattleRenderer.options:
            display = True

            # Special case code for capture, disable it if the player has no 
            # pokeballs remaining. Probably generalise when obvious what other
            # options there will be.
            if option["desc"] == "Capture" and len(self.game.game_data.player.available_pokeballs()) <= 0:
                display = False

            if display:
                actual_row = settings.SCREEN_HEIGHT + option["row"] - 1
                libtcod.console.print(self.console, x, actual_row, "{0}. {1}".format(option["char"], option["desc"]))
           
    def _render_blank_message_box(self, x: int, y: int, width: int, height: int):
        """
            Utility function to render the box in which messages go.
        """
        libtcod.console.print_frame(self.console, x, y, width, height)
           
    def _render_message(self, message, x: int, y: int):
        """
            Utility function to render a message on top of the screen at the 
            given point.
        """
        libtcod.console.print(self.console, x + 1, y + 1, message)

    def _render_pokeball_select(self, pokeballs: Dict[Pokeball, int], x: int, y: int):
        """
            Render the list of available pokeball types along with the key
            press required to select them.
        """
        for row, pokeball in enumerate(pokeballs.keys()):
            libtcod.console.print(self.console, x, y + row + 1, "{0}. {1:20s}{2}".format(pokeball.display_char, pokeball.name + " Ball", pokeballs[pokeball]))
