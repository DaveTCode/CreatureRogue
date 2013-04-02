from __future__ import division
import CreatureRogue.data as data
import CreatureRogue.settings as settings
import CreatureRogue.libtcodpy as libtcod

class BattleRenderer():
    '''
        The battle renderer is used to display a battle on the screen.
        
        It renders the entire of the screen.
    '''
    def __init__(self, game, console):
        self.game = game
        self.console = console
        
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
        libtcod.console_print(self.console, 24, 5, "LV." + str(creature.level))
        
        self._render_health_bar(creature, 28, 3, 7)

    def _render_attacking_creature_details(self, creature):
        '''
            Renders the creature box for the attacking creature.
        '''
        libtcod.console_set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(self.console, 49, 23, creature.nickname[:10])
        libtcod.console_print(self.console, 60, 23, "LV." + str(creature.level))
        
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
        max = creature.max_stat(hp_stat)
        
        libtcod.console_set_default_foreground(self.console, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(self.console, x, y, str(current) + "/" + str(max))
    
    def _render_moves(self, creature, x, y):
        ''' 
            Render the available moves for the player creature starting at
            the given x,y coordinates.
        '''
        for row in range(4):
            if row < len(creature.moves):
                move = creature.moves[row]
                
                libtcod.console_print(self.console, x, y + row, str(row + 1) + ". ")
                libtcod.console_print(self.console, x + 3, y + row, move.move_data.name)
                libtcod.console_print(self.console, x + 15, y + row, move.move_data.type.name)
                libtcod.console_print(self.console, x + 27, y + row, "(" + str(move.pp) + "/" + str(move.move_data.max_pp) + ")")
           
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