import libtcodpy as libtcod
import random
import settings
from game import Game
from pokedex_renderer import PokedexRenderer

def gen_full_pokedex(static_game_data):
    return { static_game_data.species[id].pokedex_number: (2, static_game_data.species[id]) for id in static_game_data.species }

def gen_rand_pokedex(static_game_data):
    return { static_game_data.species[id].pokedex_number: (random.randint(0,2), static_game_data.species[id]) for id in static_game_data.species }

if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.init()
    
    pokedex = gen_rand_pokedex(game.static_game_data)
    pokedex_renderer = PokedexRenderer(game.static_game_data, game.console, pokedex)
    
    while not libtcod.console_is_window_closed():
        libtcod.console_clear(game.console)
        pokedex_renderer.render()
        
        libtcod.console_blit(game.console, 0, 0, game.screen_width, game.screen_height, 0, 0, 0)
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)
        game.handle_pokedex_input(pokedex_renderer, key)