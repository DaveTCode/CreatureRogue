from __future__ import division
import settings
import libtcodpy as libtcod

class BattleRenderer():
    '''
        The battle renderer is used to display a battle on the screen.
        
        It renders the entire of the screen.
    '''
    def __init__(self, game):
        self.game = game
        
    def render(self, battle_data):
        '''
            The external interface to this class. Call this to render the
            given battle data object.
        '''
        self._render_lines()
        
        self._render_defending_creature_details(battle_data.defending_creature())
        self._render_attacking_creature_details(battle_data.player_creature)
        
        self._render_moves(battle_data.player_creature, 2, 36)
        
    def _render_lines(self):
        '''
            Renders the lines which separate sections of the screen.
        '''
        libtcod.console_set_default_foreground(0, settings.LINE_COLOR)
        libtcod.console_print_frame(0, 2, 4, 30, 6)
        libtcod.console_print_frame(0, 48, 22, 30, 8)
        libtcod.console_hline(0, 0, 34, 80)

    def _render_defending_creature_details(self, creature):
        '''
            Renders the creature box for the defending creature.
        '''
        libtcod.console_set_default_foreground(0, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(0, 3, 5, creature.nickname[:10])
        libtcod.console_print(0, 24, 5, "LV." + str(creature.level))
        
        self._render_health_bar(creature, 28, 3, 7)

    def _render_attacking_creature_details(self, creature):
        '''
            Renders the creature box for the attacking creature.
        '''
        libtcod.console_set_default_foreground(0, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(0, 49, 23, creature.nickname[:10])
        libtcod.console_print(0, 60, 23, "LV." + str(creature.level))
        
        self._render_health_bar(creature, 28, 49, 25)
        self._render_health_values(creature, 70, 27)
            
    def _render_health_bar(self, creature, max_length, x, y):
        '''
            Utility function to render a health bar for the given creature at
            the given x and y coordinates.
        '''
        hp_stat = self.game.static_game_data.hp_stat()
        health_bars = int((creature.current_stat(hp_stat) / creature.max_stat(hp_stat)) * max_length)
        
        if (health_bars > max_length / 2):
            color = settings.GOOD_HEALTH_COLOR
        elif (health_bars > max_length / 4):
            color = settings.HALF_HEALTH_COLOR
        else:
            color = settings.LOW_HEALTH_COLOR
            
        libtcod.console_set_default_foreground(0, color)
        for i in range(x, x + health_bars):
            libtcod.console_put_char(0, i, y, '=')
            
        libtcod.console_set_default_foreground(0, settings.BLANK_HEALTH_COLOR)
        for i in range(x + health_bars, x + max_length):
            libtcod.console_put_char(0, i, y, '=')
            
    def _render_health_values(self, creature, x, y):
        '''
            Utility function to render the health values <current>/<max> at 
            the given x,y coordinates.
        '''
        hp_stat = self.game.static_game_data.hp_stat()
        current = creature.current_stat(hp_stat)
        max = creature.current_stat(hp_stat)
        
        libtcod.console_set_default_foreground(0, settings.BATTLE_TEXT_COLOR)
        libtcod.console_print(0, x, y, str(current) + "/" + str(max))
    
    def _render_moves(self, creature, x, y):
        ''' 
            Render the available moves for the player creature starting at
            the given x,y coordinates.
        '''
        chars = ['A. ', 'B. ', 'C. ', 'D. ']
        
        for row in range(4):
            move = creature.moves[row]
                
            libtcod.console_print(0, x, y + row, chars[row])
            libtcod.console_print(0, x + 3, y + row, move["move"].name)
            libtcod.console_print(0, x + 15, y + row, move["move"].type.name)
            libtcod.console_print(0, x + 27, y + row, "(" + str(move["pp"]) + "/" + str(move["move"].max_pp) + ")")
            
    def _render_message(self, message, x, y):
        '''
            Utility function to render a message on top of the screen at the 
            given point.
        '''
        pass