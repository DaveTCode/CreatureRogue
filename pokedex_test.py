"""
    Used to test the game pokedex state. Allows a user to view a random 
    pokedex. 

    Will crash on exiting the pokedex as the game will not have been 
    set up (this is intentional).
"""
import random

import CreatureRogue.settings as settings
from CreatureRogue.game import Game
from CreatureRogue.models.player import Player
from CreatureRogue.pokedex_renderer import PokedexRenderer
from CreatureRogue.pokedex_state import PokedexState


def gen_full_pokedex(static_game_data):
    return {static_game_data.species[id].pokedex_number: (2, static_game_data.species[id]) for id in
            static_game_data.species}


def gen_rand_pokedex(static_game_data):
    return {static_game_data.species[id].pokedex_number: (random.randint(0, 2), static_game_data.species[id]) for id in
            static_game_data.species}


if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.load_static_data()
    game.init()

    pokedex_renderer = PokedexRenderer(game)

    game.game_data.player = Player("Pokedex test player", game.static_game_data, None, 0, 0)  # Don't need to set map,x,y on pokedex test player
    game.game_data.player.pokedex = gen_rand_pokedex(game.static_game_data)
    game.state = PokedexState(game, game.game_data, pokedex_renderer)

    game.game_loop()
