import random
from game import Game
from models import GameData, BattleData, Creature, Move, BattleCreature
import settings
import libtcodpy as libtcod

def random_stat_values(stats, min, max):
    return {stats[stat]: random.randint(min, max) for stat in stats}
    
def zero_stat_values(stats):
    return {stats[stat]: 0 for stat in stats}

if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
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
    defending_moves = [Move(move_data) for move_data in defending_species.move_data_at_level(defending_level)]

    game_data.battle_data = BattleData(game_data, 
                                       BattleCreature(Creature(attacking_species, attacking_level, None, None, random_stat_values(game.static_game_data.stats, 1, 15), zero_stat_values(game.static_game_data.stats), False, attacking_moves, 1), game.static_game_data),
                                       wild_creature=BattleCreature(Creature(defending_species, defending_level, None, None, random_stat_values(game.static_game_data.stats, 1, 15), zero_stat_values(game.static_game_data.stats), False, defending_moves, 1), game.static_game_data))
    
    while not libtcod.console_is_window_closed():
        game.battle_renderer.render(game_data.battle_data)

        libtcod.console_blit(game.console, 0, 0, game.screen_width, game.screen_height, 0, 0, 0)
        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)
        game.handle_input(game_data, key)