import random
from game import Game
from models import GameData, BattleData, Creature
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
    game_data.is_in_battle = True
    
    attacking_id = int(raw_input("Enter the pokedex number of the attacking creature: "))
    attacking_species = game.static_game_data.species[attacking_id]
    print("You've select a: " + str(attacking_species))
    
    defending_id = int(raw_input("Enter the pokedex number of the defending creature: "))
    defending_species = game.static_game_data.species[defending_id]
    print("You've select a: " + str(defending_species))
    
    attacking_moves = [game.static_game_data.moves[1], game.static_game_data.moves[2], game.static_game_data.moves[3], game.static_game_data.moves[4]]
    
    game_data.battle_data.player_creature = Creature(attacking_species, 1, None, None, random_stat_values(game.static_game_data.stats, 1, 15), zero_stat_values(game.static_game_data.stats), False, attacking_moves, 1)
    game_data.battle_data.wild_creature = Creature(defending_species, 1, None, None, random_stat_values(game.static_game_data.stats, 1, 15), zero_stat_values(game.static_game_data.stats), False, [], 1)
    
    game_data.battle_data.wild_creature.stats[game.static_game_data.hp_stat()] = 5
    
    while not libtcod.console_is_window_closed():
        game.render(game_data)

        libtcod.console_flush()
        key = libtcod.console_wait_for_keypress(True)
        game.handle_input(game_data, key)