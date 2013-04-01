import argparse

from maps.map_renderer import MapRenderer
import maps.kanto as kanto
from models import Map, Player, Creature, BattleCreature, Move
from game import Game
from map_state import MapState
import settings
import libtcodpy as libtcod
import creature_creator

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    args = parser.parse_args()

    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.load_static_data()
    game.init()

    game.game_data.player = Player("Test Player", game.static_game_data, Map(kanto.name, kanto.tiles), args.x, args.y)
    game.state = MapState(game, game.game_data, game.map_renderer)

    attacking_id = int(raw_input("Enter the pokedex number of the player creature: "))
    attacking_level = int(raw_input("Enter the level of the player creature: "))
    attacking_species = game.static_game_data.species[attacking_id]
    print("You've selected a: Lv." + str(attacking_level) + " " + str(attacking_species))

    attacking_moves = [Move(move_data) for move_data in attacking_species.move_data_at_level(attacking_level)]

    game.game_data.player.creatures.append(Creature(attacking_species, attacking_level, None, None, creature_creator.random_stat_values(game.static_game_data.stats, 1, 15), creature_creator.zero_stat_values(game.static_game_data.stats), False, attacking_moves, 1))

    game.game_loop()