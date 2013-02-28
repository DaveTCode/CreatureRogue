from __future__ import division
import sys
import libtcodpy as libtcod
import db_layer
import settings
from models import GameData, Player

class Game():
    
    def __init__(self, screen_width, screen_height, title, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        self.font = font
        self.static_game_data = None
    
    def init(self):
        '''
            Set up the libtcod window with the parameters given to the game. 
            This must be called before the game loop is run.
        '''
        libtcod.console_set_custom_font(self.font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        
        libtcod.console_init_root(self.screen_width, self.screen_height, self.title, False)
        
        self.static_game_data = db_layer.Loader(settings.DB_FILE).load_static_data()
    
    def game_loop(self):
        '''
            The game loop runs until the user closes the window manually. All 
            game logic and rendering is done here.
        '''
        game_data = GameData()
        
        while not libtcod.console_is_window_closed():
            self.render(game_data)
            
            key = libtcod.console_wait_for_keypress(True)
            self.handle_input(key)
            
    def render(self, game_data):
        libtcod.console_set_default_foreground(0, libtcod.white)
        
        if game_data.is_in_battle:
            self.render_battle(game_data.battle_data)
        else:
            self.render_world(game_data)
        
        libtcod.console_flush()
        
    def render_battle(self, battle):
        def render_lines():
            libtcod.console_set_default_foreground(0, settings.LINE_COLOR)
            libtcod.console_print_frame(0, 2, 4, 30, 6)
            libtcod.console_print_frame(0, 48, 22, 30, 8)
            libtcod.console_hline(0, 0, 34, 80)
    
        def render_defending_creature_details(creature):
            libtcod.console_set_default_foreground(0, settings.BATTLE_TEXT_COLOR)
            libtcod.console_print(0, 3, 5, creature.nickname[:10])
            libtcod.console_print(0, 24, 5, "LV." + str(creature.level))
            
            render_health_bar(creature, 28, 3, 7)
    
        def render_attacking_creature_details(creature):
            libtcod.console_set_default_foreground(0, settings.BATTLE_TEXT_COLOR)
            libtcod.console_print(0, 49, 23, creature.nickname[:10])
            libtcod.console_print(0, 60, 23, "LV." + str(creature.level))
            
            render_health_bar(creature, 28, 49, 25)
                
        def render_health_bar(creature, max_length, x, y):
            hp_stat = self.static_game_data.hp_stat()
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
        
        render_lines()
        
        render_defending_creature_details(battle.defending_creature())
        render_attacking_creature_details(battle.player_creature)
        
    def render_world(self, game_data):
        pass
        
    def handle_input(self, key):
        '''
            Handles a single key stroke.
        '''
        if key.vk == libtcod.KEY_ESCAPE:
            sys.exit(0)