'''
    When creating wild creatures their available moves and stats are able to 
    be calculated deterministically.

    This module provides a single interface for doing that using 
    create_wild_creature.
'''
import random
from CreatureRogue.models.creature import Creature
from CreatureRogue.models.move import Move

def random_stat_values(stats, min_val, max_val):
    '''
        Used to return a set of random values between min, max for
        all available stats.
    '''
    return {stats[stat]: random.randint(min_val, max_val) for stat in stats}
    
def zero_stat_values(stats):
    '''
        Used to return a set of zero values for all stats.
    '''
    return {stats[stat]: 0 for stat in stats}

def create_wild_creature(static_game_data, species, level):
    '''
        Creating a wild creature of a given species and level is nearly 
        deterministic. The only randomization is in the individual individual
        values as these determine any variation from the species base.
    '''
    moves = [Move(move) for move in species.move_data_at_level(level)]

    return Creature(species, 
                    level, 
                    None, 
                    None, 
                    random_stat_values(static_game_data.stats, 1, 15), 
                    zero_stat_values(static_game_data.stats), 
                    False, 
                    moves,
                    static_game_data.xp_lookup.xp_at_level(species, level))