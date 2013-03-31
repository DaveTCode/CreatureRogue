from maps.map_renderer import MapRenderer
import maps.kanto as kanto
from models import Map, Player
from game import Game
from map_state import MapState
import settings
import libtcodpy as libtcod

if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.load_static_data()
    game.init()
    
    game.game_data.player = Player("Test Player", game.static_game_data, Map(kanto.name, kanto.tiles), 11, 23)
    game.state = MapState(game, game.game_data, game.map_renderer)

    game.game_loop()