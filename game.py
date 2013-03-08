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
        self.battle_renderer = None
        self.console = None
    
    def init(self):
        '''
            Set up the libtcod window with the parameters given to the game. 
            This must be called before the game loop is run.
        '''
        libtcod.console_set_custom_font(self.font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        
        libtcod.console_init_root(self.screen_width, self.screen_height, self.title, False)
        self.console = libtcod.console_new(self.screen_width, self.screen_height)
        self.battle_renderer = BattleRenderer(self, self.console)
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
        libtcod.console_set_default_foreground(self.console, libtcod.white)
        libtcod.console_print_frame(self.console, 0, 0, self.screen_width, self.screen_height)
        
        if game_data.is_in_battle:
            self.battle_renderer.render(game_data.battle_data)
        else:
            self.render_world(game_data)
        
        libtcod.console_blit(self.console, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
        libtcod.console_flush()
        
    def render_world(self, game_data):
        pass
        
    def handle_input(self, game_data, key):
        '''
            Handles a single key stroke.
        '''        
        if game_data.is_in_battle:
            self.handle_battle_input(game_data.battle_data, key)
        else:
            pass
            
    def handle_map_input(self, player, key):
        '''
            Handles a single key stroke when the player is traversing the map.
        '''
        x_delta, y_delta = 0,0
        if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
            x_delta = -1
        elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
            x_delta = 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_UP):
            y_delta = -1
        elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
            y_delta = 1
        
        if x_delta != 0 or y_delta != 0:
            new_y, new_x = y_delta + player.coords[1], x_delta + player.coords[0]
            next_cell = None
            
            try:
                next_cell = player.map.tiles[new_y][new_x]
                
                if player.can_traverse(next_cell):
                    player.move_to_cell(new_x, new_y)
            except KeyError:
                pass
            
    def handle_battle_input(self, battle_data, key):
        if len(battle_data.messages_to_display) > 0:
            if libtcod.console_is_key_pressed(libtcod.KEY_SPACE) or libtcod.console_is_key_pressed(libtcod.KEY_ENTER):
                battle_data.pop_message()
        else:
            move = None
            for (key_code, index) in [(libtcod.KEY_1, 0), (libtcod.KEY_2, 1), (libtcod.KEY_3, 2), (libtcod.KEY_4, 3)]:
                if libtcod.console_is_key_pressed(key_code):
                    if len(battle_data.player_creature.creature.moves) > index:
                        move = battle_data.player_creature.creature.moves[index]
                
            if move != None:
                messages = move.act(battle_data.player_creature, battle_data.defending_creature(), self.static_game_data)
                for message in messages:
                    battle_data.messages_to_display.append(message)
                    
    def handle_pokedex_input(self, pokedex_renderer, key):
        if pokedex_renderer.displaying_species():
            if libtcod.console_is_key_pressed(libtcod.KEY_ESCAPE):
                pokedex_renderer.close_display()
        else:
            if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
                pokedex_renderer.shift_column(-1)
            elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
                pokedex_renderer.shift_column(1)
            elif libtcod.console_is_key_pressed(libtcod.KEY_UP):
                pokedex_renderer.shift_row(-1)
            elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
                pokedex_renderer.shift_row(1)
            elif libtcod.console_is_key_pressed(libtcod.KEY_ENTER):
                pokedex_renderer.display_selected()