from map_renderer import MapRenderer
from models import Map, Player
from game import Game
import settings
import maps
import libtcodpy as libtcod

if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.init()
    
    map_renderer = MapRenderer(game.console)
    player = Player("Test Player", game.static_game_data, Map(game.static_game_data.location_areas[1], maps.PalletTown), 3, 3)
    
    while not libtcod.console_is_window_closed():
        libtcod.console_clear(game.console)
        map_renderer.render(player)
        
        libtcod.console_blit(game.console, 0, 0, game.screen_width, game.screen_height, 0, 0, 0)
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)
        game.handle_map_input(player, key)