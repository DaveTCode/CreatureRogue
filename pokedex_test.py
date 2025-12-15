"""
Used to test the game pokedex state. Allows a user to view a random
pokedex.

Will crash on exiting the pokedex as the game will not have been
set up (this is intentional).
"""

import random

from CreatureRogue.game import Game
from CreatureRogue.models.player import Player
from CreatureRogue.states.pokedex_state import PokedexState


def gen_full_pokedex(static_game_data):
    return {
        static_game_data.species[id].pokedex_number: (2, static_game_data.species[id])
        for id in static_game_data.species
    }


def gen_rand_pokedex(static_game_data):
    return {
        static_game_data.species[id].pokedex_number: (
            random.randint(0, 2),
            static_game_data.species[id],
        )
        for id in static_game_data.species
    }


if __name__ == "__main__":
    game = Game.create()

    game.game_data.player = Player(
        "Pokedex test player", game.static_game_data, None, 0, 0
    )  # Don't need to set map,x,y on pokedex test player
    game.game_data.player.pokedex = gen_rand_pokedex(game.static_game_data)
    game.state = PokedexState(game, game.game_data, game.pokedex_renderer)

    game.game_loop()
