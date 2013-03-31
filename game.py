from __future__ import division
import sys
import libtcodpy as libtcod
import db_layer
import settings
from models import GameData, Player
from battle_renderer import BattleRenderer
from maps.map_renderer import MapRenderer
from pokedex_renderer import PokedexRenderer
from map_state import MapState
from battle_state import BattleState
from pokedex_state import PokedexState

class Game():
    
    def __init__(self, screen_width, screen_height, title, font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        self.font = font
        self.static_game_data = None
    
    def load_static_data(self):
        '''
            This is required all over and must be called before init is called
            to create the renderers.
        '''
        self.static_game_data = db_layer.Loader(settings.DB_FILE).load_static_data()

    def init(self):
        '''
            Set up the libtcod window with the parameters given to the game. 
            This must be called before the game loop is run.
        '''
        if self.static_game_data == None:
            print("You must load the static game data before calling init")
            sys.exit(1)
            
        libtcod.console_set_custom_font(self.font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(self.screen_width, self.screen_height, self.title, False)
        libtcod.sys_set_fps(settings.FPS_LIMIT)

        self.console = libtcod.console_new(self.screen_width, self.screen_height)

        self.game_data = GameData()

        self.battle_renderer = BattleRenderer(self, self.console)
        self.map_renderer = MapRenderer(self, self.console)
        self.pokedex_renderer = PokedexRenderer(self, self.console)
        
        self.state = MapState(self, self.game_data, self.map_renderer)
    
    def game_loop(self):
        '''
            The game loop runs until the user closes the window manually. All 
            game logic and rendering is done here.
        '''
        while not libtcod.console_is_window_closed():
            libtcod.console_set_default_foreground(self.console, libtcod.white)
            libtcod.console_print_frame(self.console, 0, 0, self.screen_width, self.screen_height)
            
            self.state.render()

            libtcod.console_blit(self.console, 0, 0, self.screen_width, self.screen_height, 0, 0, 0)
            libtcod.console_flush()

            key = libtcod.console_check_for_keypress()
            if key and key.vk != libtcod.KEY_NONE:
                self.state.handle_input(key)