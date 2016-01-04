"""
    Script used to test the battle state functionality. Allows the user to pick
    a pair of creatures and then uses the game loop to fight them.

    Will probably crash when the battle concludes because the rest of the game
    will not be set up at that point.
"""
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
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.load_static_data()
    game.init()
    
    game_data = GameData()
    
    attacking_id = int(input("Enter the pokedex number of the attacking creature: "))
    attacking_level = int(input("Enter the level of the attacking creature: "))
    attacking_species = game.static_game_data.species[attacking_id]
    print("You've selected a: Lv." + str(attacking_level) + " " + str(attacking_species))
    
    defending_id = int(input("Enter the pokedex number of the defending creature: "))
    defending_level = int(input("Enter the level of the defending creature: "))
    defending_species = game.static_game_data.species[defending_id]
    print("You've selected a: Lv." + str(defending_level) + " " + str(defending_species))
    
    attacking_moves = [Move(move_data) for move_data in attacking_species.move_data_at_level(attacking_level)]

    wild_creature = BattleCreature(creature_creator.create_wild_creature(game.static_game_data, defending_species, defending_level), game.static_game_data)

    game_data.battle_data = BattleData(game_data, 
                                       BattleCreature(Creature(attacking_species, attacking_level, None, None, creature_creator.random_stat_values(game.static_game_data.stats, 1, 15), creature_creator.zero_stat_values(game.static_game_data.stats), False, attacking_moves, 1), game.static_game_data),
                                       RandomMoveAi(wild_creature),
                                       wild_creature=wild_creature)
    game_data.player = Player("Test", game.static_game_data, None, 0, 0)
    game_data.player.pokeballs[game.static_game_data.pokeballs[1]] = 3
    game.game_data = game_data
    game.state = BattleState(game, game.game_data, game.battle_renderer, game.level_up_renderer, game.catch_graphic_renderer)
    game.game_loop()
