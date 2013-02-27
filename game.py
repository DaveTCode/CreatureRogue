import sys
import libtcodpy as libtcod
import db_layer
import settings

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
        game_data = None
        
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
        #libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE) # Tester code
        
        libtcod.console_flush()
        
    def render_battle(self, battle):
        pass
        
    def render_world(self, game_data):
        pass
        
    def handle_input(self, key):
        '''
            Handles a single key stroke.
        '''
        if key.vk == libtcod.KEY_ESCAPE:
            sys.exit(0)