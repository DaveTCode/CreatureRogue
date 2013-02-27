class Creature():
    
    def __init__(self, species, level, nickname, trainer, individual_values, effort_values, was_traded, moves, stats):
        self.species = species
        self.level = level
        self.nickname = nickname
        self.trainer = trainer
        self.individual_values = individual_values
        self.effort_values = effort_values
        self.was_traded = was_traded
        self.moves = [{'move': move, 'pp': move.max_pp} for move in moves]
        self.stats = stats
        
        self.current_hp = self.max_hp()
        
    def max_stat(self, stat):
        '''
            The stat value of a creature is a function of it's level, species,
            IVs and EVs and differs slightly for hitpoints and normal stats.
        '''
        if stat.name = "hp":
            value = (self.individual_values[stat] + self.species.base_stats[stat] + math.sqrt(self.effort_values[stat]) / 8 + 50) * self.level / 50 + 10
        else:
            value = (self.individual_values[stat] + self.species.base_stats[stat] + math.sqrt(self.effort_values[stat]) / 8) * self.level / 50 + 5
            
        return int(math.floor(value))
        
    def xp_given(self, number_winners, winner_traded, winner_modifier = 1):
        '''
            This corresponds to the number of experience points gained for 
            defeating this creature.
        '''
        xp = self.species.base_xp_yield * winner_modifier * self.level / (7 * number_winners)
        if self.trainer != None:
            xp = xp * 1.5
        if winner_traded:
            xp = xp * 1.5
        
        return math.floor(xp)
        
class Player():

    def __init__(self, name, creatures):
        self.name = name
        self.creatures = creatures
        
class GameData():
        
    def __init__(self, player):
        self.player = player
        self.is_in_battle = False
        
class BattleData():

    def __init__(self, game_data, player_pokemon, trainer_pokemon=None, wild_pokemon=None):
        self.game_data = game_data
        self.player_pokemon = player_pokemon
        self.wild_pokemon = wild_pokemon
        self.trainer_pokemon = trainer_pokemon