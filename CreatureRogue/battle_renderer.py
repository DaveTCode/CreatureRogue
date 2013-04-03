'''
    Module contains all renderers which are used in battle
'''
from __future__ import division
import CreatureRogue.data as data
import CreatureRogue.settings as settings
import CreatureRogue.libtcodpy as libtcod

class LevelUpRenderer():
    '''
        The level up renderer is used for rendering an overlay on top of the
        battle renderer indicating stat changes on level up.

        Whilst it's not technically an independent renderer it can still be 
        used as one if required.
    '''

    width = 35
    height = 13
    
    def __init__(self, game):
        self.game = game
        self.console = libtcod.console_new(LevelUpRenderer.width, LevelUpRenderer.height)

    def render(self, creature, prev_level):
        '''
            Returns a full console that can be blitted onto something else
            anywhere the calling code chooses.
        '''
        libtcod.console_clear(self.console)
        libtcod.console_set_default_background(self.console, settings.LEVEL_UP_BG_COLOR)
        self._render_lines()
        self._render_summary(creature, prev_level)
        self._render_stats(creature, prev_level)

        return self.console

    def _render_lines(self):
        libtcod.console_print_frame(self.console, 1, 1, LevelUpRenderer.width - 2, LevelUpRenderer.height - 2)

    def _render_summary(self, creature, prev_level):
        summary_str = "Level {0} -> {1}".format(prev_level, creature.level)
        libtcod.console_set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(self.console, 5, 3, summary_str)

    def _render_stats(self, creature, prev_level):
        libtcod.console_set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)

        for idx, stat in enumerate([stat for stat in creature.stats if stat.short_name != None and stat.short_name != ""]):
            stat_str = "{0:7s}: {1:3d} -> {2:3d}".format(stat.short_name, creature.max_stat(stat, level=prev_level), creature.max_stat(stat))

            libtcod.console_print(self.console, 5, 4 + idx, stat_str)

class BattleRenderer():
    '''
        The battle renderer is used to display a battle on the screen.
        
        It renders the entire of the screen.
    '''
    def __init__(self, game):
        self.game = game
        self.console = libtcod.console_new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        
    def render(self, battle_data, messages):
        '''
            The external interface to this class. Call this to render the
            given battle data object.
        '''
        self._render_lines()
        
        self._render_defending_creature_details(battle_data.defending_creature().creature)
        self._render_attacking_creature_details(battle_data.player_creature.creature)
        
        self._render_moves(battle_data.player_creature.creature, 2, 36)
        
        self._render_blank_message_box(40, 34, 40, 16)
        if len(messages):
            self._render_message(messages[0], 40, 38, 40, 12)

        return self.console
        
    def _render_lines(self):
        '''
            Renders the lines which separate sections of the screen.
        '''
        libtcod.console_set_default_foreground(self.console, settings.LINE_COLOR)
        libtcod.console_print_frame(self.console, 2, 4, 30, 6)
        libtcod.console_print_frame(self.console, 48, 22, 30, 8)
        libtcod.console_hline(self.console, 0, 34, 80)

    def _render_defending_creature_details(self, creature):
        '''
            Renders the creature box for the defending creature.
        '''
        libtcod.console_set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(self.console, 3, 5, creature.nickname[:10])
        libtcod.console_print(self.console, 24, 5, "LV.{0}".format(creature.level))
        
        self._render_health_bar(creature, 28, 3, 7)

    def _render_attacking_creature_details(self, creature):
        '''
            Renders the creature box for the attacking creature.
        '''
        libtcod.console_set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(self.console, 49, 23, creature.nickname[:10])
        libtcod.console_print(self.console, 60, 23, "LV.{0}".format(creature.level))
        
        self._render_health_bar(creature, 28, 49, 25)
        self._render_health_values(creature, 70, 27)
            
    def _render_health_bar(self, creature, max_length, x, y):
        '''
            Utility function to render a health bar for the given creature at
            the given x and y coordinates.
        '''
        hp_stat = self.game.static_game_data.stat(data.HP_STAT)
        health_bars = int((creature.current_stat(hp_stat) / creature.max_stat(hp_stat)) * max_length)
        
        if (health_bars > max_length / 2):
            color = settings.GOOD_HEALTH_COLOR
        elif (health_bars > max_length / 4):
            color = settings.HALF_HEALTH_COLOR
        else:
            color = settings.LOW_HEALTH_COLOR
            
        libtcod.console_set_default_foreground(self.console, color)
        for i in range(x, x + health_bars):
            libtcod.console_put_char(self.console, i, y, '=')
            
        libtcod.console_set_default_foreground(self.console, settings.BLANK_HEALTH_COLOR)
        for i in range(x + health_bars, x + max_length):
            libtcod.console_put_char(self.console, i, y, '=')
            
    def _render_health_values(self, creature, x, y):
        '''
            Utility function to render the health values <current>/<max> at 
            the given x,y coordinates.
        '''
        hp_stat = self.game.static_game_data.stat(data.HP_STAT)
        current = creature.current_stat(hp_stat)
        max_hp = creature.max_stat(hp_stat)
        
        libtcod.console_set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(self.console, x, y, "{0}/{1}".format(current, max_hp))
    
    def _render_moves(self, creature, x, y):
        ''' 
            Render the available moves for the player creature starting at
            the given x,y coordinates.
        '''
        for row in range(4):
            if row < len(creature.moves):
                move = creature.moves[row]
                
                libtcod.console_print(self.console, x, y + row, "{0}. ".format(row + 1))
                libtcod.console_print(self.console, x + 3, y + row, move.move_data.name)
                libtcod.console_print(self.console, x + 15, y + row, move.move_data.type.name)
                libtcod.console_print(self.console, x + 27, y + row, "({0}/{1})".format(move.pp, move.move_data.max_pp))
           
    def _render_blank_message_box(self, x, y, width, height):
        '''
            Utility function to render the box in which messages go.
        '''
        libtcod.console_print_frame(self.console, x, y, width, height)
           
    def _render_message(self, message, x, y, width, height):
        '''
            Utility function to render a message on top of the screen at the 
            given point.
        '''
        libtcod.console_print(self.console, x + 1, y + 1, message)