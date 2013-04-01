import random
from game import Game
from models import GameData, BattleData, Creature, Move, BattleCreature
from battle_state import BattleState
from battle_ai import RandomMoveAi
import settings
import libtcodpy as libtcod
import creature_creator

if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.load_static_data()
    game.init()
    
    game_data = GameData()
    
    attacking_id = int(raw_input("Enter the pokedex number of the attacking creature: "))
    attacking_level = int(raw_input("Enter the level of the attacking creature: "))
    attacking_species = game.static_game_data.species[attacking_id]
    print("You've selected a: Lv." + str(attacking_level) + " " + str(attacking_species))
    
    defending_id = int(raw_input("Enter the pokedex number of the defending creature: "))
    defending_level = int(raw_input("Enter the level of the defending creature: "))
    defending_species = game.static_game_data.species[defending_id]
    print("You've selected a: Lv." + str(defending_level) + " " + str(defending_species))
    
    attacking_moves = [Move(move_data) for move_data in attacking_species.move_data_at_level(attacking_level)]

    wild_creature = BattleCreature(creature_creator.create_wild_creature(game.static_game_data, defending_species, defending_level), game.static_game_data)

    game_data.battle_data = BattleData(game_data, 
                                       BattleCreature(Creature(attacking_species, attacking_level, None, None, creature_creator.random_stat_values(game.static_game_data.stats, 1, 15), creature_creator.zero_stat_values(game.static_game_data.stats), False, attacking_moves, 1), game.static_game_data),
                                       RandomMoveAi(wild_creature),
                                       wild_creature=wild_creature)
    
    game.game_data = game_data
    game.state = BattleState(game, game.game_data, game.battle_renderer)
    game.game_loop()