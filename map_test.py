import argparse

import CreatureRogue.creature_creator as creature_creator
import CreatureRogue.settings as settings
from CreatureRogue.game import Game
from CreatureRogue.models.creature import Creature
from CreatureRogue.data_layer.map_loader import MapLoader
from CreatureRogue.data_layer.region import Region
from CreatureRogue.models.move import Move
from CreatureRogue.models.player import Player
from CreatureRogue.states.map_state import MapState

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=int)
    parser.add_argument("y", type=int)
    # TODO - Allow for selection of other regions (when they're stored in the database
    args = parser.parse_args()

    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.load_static_data()
    game.init()

    # TODO - Fix this now that the map data isn't loaded automatically
    kanto_region = Region(region_id=1, identifier="kanto", name="kanto")
    map_data = MapLoader(db_file=settings.DB_FILE).load_map(region=kanto_region,
                                                            tile_types=game.static_game_data.map_data_tile_types,
                                                            default_tile_type=game.static_game_data.map_data_tile_types[11])
    game.game_data.player = Player("Test Player", game.static_game_data, map_data, args.x, args.y)
    game.state = MapState(game, game.game_data, game.map_renderer)

    attacking_id = int(input("Enter the pokedex number of the player creature: "))
    attacking_level = int(input("Enter the level of the player creature: "))
    attacking_species = game.static_game_data.species[attacking_id]
    print("You've selected a: Lv." + str(attacking_level) + " " + str(attacking_species))

    attacking_moves = [Move(move_data) for move_data in attacking_species.move_data_at_level(attacking_level)]

    game.game_data.player.creatures.append(Creature(attacking_species, attacking_level, None, None, creature_creator.random_stat_values(game.static_game_data.stats, 1, 15), creature_creator.zero_stat_values(game.static_game_data.stats), False, attacking_moves, 1))
    # game.game_data.player.pokeballs[game.game_data.player.pokeballs.keys()[0]] = 100

    game.game_loop()
