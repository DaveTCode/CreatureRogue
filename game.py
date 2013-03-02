from __future__ import division
import sys
import libtcodpy as libtcod
import db_layer
import settings
from models import GameData, Player
from battle_renderer import BattleRenderer

class Game():
    
    def __init__(self, screen_width, screen_height, title, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        self.font = font
        self.static_game_data = None
        self.battle_renderer = BattleRenderer(self)
    
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
            self.handle_input(game_data, key)
            
    def render(self, game_data):
        libtcod.console_set_default_foreground(0, libtcod.white)
        
        if game_data.is_in_battle:
            self.battle_renderer.render(game_data.battle_data)
        else:
            self.render_world(game_data)
        
        libtcod.console_flush()
        
    def render_world(self, game_data):
        pass
        
    def handle_input(self, game_data, key):
        '''
            Handles a single key stroke.
        '''
        if key.vk == libtcod.KEY_ESCAPE:
            sys.exit(0)
        
        if game_data.is_in_battle:
            self.handle_battle_input(game_data.battle_data, key)
        else:
            pass
            
    def handle_battle_input(self, battle_data, key):
        if len(battle_data.messages_to_display) > 0:
            if libtcod.console_is_key_pressed(libtcod.KEY_SPACE) or libtcod.console_is_key_pressed(libtcod.KEY_ENTER):
                battle_data.pop_message()
        else:
            move = None
            if libtcod.console_is_key_pressed(libtcod.KEY_CHAR):
                if key.c == ord('a'):
                    move = battle_data.player_creature.creature.moves[0]
                elif key.c == ord('b'):
                    move = battle_data.player_creature.creature.moves[1]
                elif key.c == ord('c'):
                    move = battle_data.player_creature.creature.moves[2]
                elif key.c == ord('d'):
                    move = battle_data.player_creature.creature.moves[3]
                
            if move != None:
                messages = move.act(battle_data.player_creature, battle_data.defending_creature(), self.static_game_data)
                for message in messages:
                    battle_data.messages_to_display.append(message)