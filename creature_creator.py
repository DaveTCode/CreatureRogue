import random
from models import Creature, Move

def random_stat_values(stats, min, max):
    return {stats[stat]: random.randint(min, max) for stat in stats}
    
def zero_stat_values(stats):
    return {stats[stat]: 0 for stat in stats}

def create_wild_creature(static_game_data, species, level):
    '''
        Creating a wild creature of a given species and level is nearly 
        deterministic. The only randomization is in the individual individual
        values as these determine any variation from the species base.
    '''
    moves = map(lambda m: Move(m), species.move_data_at_level(level))

    return Creature(species, 
                    level, 
                    None, 
                    None, 
                    random_stat_values(static_game_data.stats, 1, 15), 
                    zero_stat_values(static_game_data.stats), 
                    False, 
                    moves,
                    1) # DAT - xp here is wrong