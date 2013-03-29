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
        self.battle_renderer = None
        self.console = None
        self.state = None
    
    def init(self):
        '''
            Set up the libtcod window with the parameters given to the game. 
            This must be called before the game loop is run.
        '''
        libtcod.console_set_custom_font(self.font, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(self.screen_width, self.screen_height, self.title, False)
        libtcod.sys_set_fps(settings.FPS_LIMIT)

        self.console = libtcod.console_new(self.screen_width, self.screen_height)
        self.battle_renderer = BattleRenderer(self, self.console)
        self.map_renderer = MapRenderer(self, self.console)
        self.static_game_data = db_layer.Loader(settings.DB_FILE).load_static_data()
        self.game_data = GameData()
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

    def start_wild_batle(self):
        self.game_data.is_in_battle = True
        self.game_data.battle_data = BattleData(self.game_data, self.player, wild_creature = self.player.location_area.get_encounter_creature())