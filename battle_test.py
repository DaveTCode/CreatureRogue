"""
    Script used to test the battle state functionality. Allows the user to pick
    a pair of creatures and then uses the game loop to fight them.

    Will probably crash when the battle concludes because the rest of the game
    will not be set up at that point.
"""
import argparse

import CreatureRogue.creature_creator as creature_creator
import CreatureRogue.settings as settings
from CreatureRogue.battle_ai import RandomMoveAi
from CreatureRogue.game import Game
from CreatureRogue.models.battle_creature import BattleCreature
from CreatureRogue.models.battle_data import BattleData
from CreatureRogue.models.creature import Creature
from CreatureRogue.models.game_data import GameData
from CreatureRogue.models.move import Move
from CreatureRogue.models.player import Player
from CreatureRogue.states.battle_state import BattleState

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("attacking_creature_id", type=int)
    parser.add_argument("attacking_creature_level", type=int)
    parser.add_argument("defending_creature_id", type=int)
    parser.add_argument("defending_creature_level", type=int)
    args = parser.parse_args()

    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.load_static_data()
    game.init()
    
    game_data = GameData()
    
    attacking_species = game.static_game_data.species[args.attacking_creature_id]
    print("You've selected a: Lv.{0} {1}".format(args.attacking_creature_level, attacking_species))

    defending_species = game.static_game_data.species[args.defending_creature_id]
    print("You've selected a: Lv.{0} {1}".format(args.defending_creature_level, defending_species))
    
    attacking_moves = [Move(move_data) for move_data in attacking_species.move_data_at_level(args.attacking_creature_level)]

    wild_creature = BattleCreature(creature_creator.create_wild_creature(game.static_game_data, defending_species, args.defending_creature_level), game.static_game_data)

    game_data.battle_data = BattleData(game_data, 
                                       BattleCreature(Creature(attacking_species, args.attacking_creature_level, None, None, creature_creator.random_stat_values(game.static_game_data.stats, 1, 15), creature_creator.zero_stat_values(game.static_game_data.stats), False, attacking_moves, 1), game.static_game_data),
                                       RandomMoveAi(wild_creature),
                                       wild_creature=wild_creature)
    game_data.player = Player("Test", game.static_game_data, None, 0, 0)
    game_data.player.pokeballs[game.static_game_data.pokeballs[1]] = 3
    game.game_data = game_data
    game.state = BattleState(game, game.game_data, game.battle_renderer, game.level_up_renderer, game.catch_graphic_renderer)
    game.game_loop()
