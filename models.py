from __future__ import division
import math
import sys

class Creature():
    
    def __init__(self, species, level, nickname, trainer, individual_values, effort_values, was_traded, moves, current_xp):
        self.species = species
        self.level = level
        self.nickname = nickname if nickname != None else species.name
        self.trainer = trainer
        self.individual_values = individual_values
        self.effort_values = effort_values
        self.was_traded = was_traded
        self.moves = [{'move': move, 'pp': move.max_pp} for move in moves]
        self.stats = {stat: self.max_stat(stat) for stat in species.base_stats}
        self.current_xp = current_xp
        
    def adjust_stat(self, stat, delta):
        self.stats[stat] = self.stats[stat] - delta
        
        if self.stats[stat] < 0:
            self.stats[stat] = 0
        elif self.stats[stat] > self.max_stat(stat):
            self.stats[stat] = self.max_stat(stat)
        
    def current_stat(self, stat):
        return self.stats[stat]
        
    def max_stat(self, stat):
        '''
            The stat value of a creature is a function of it's level, species,
            IVs and EVs and differs slightly for hitpoints and normal stats.
        '''
        if stat.name.upper() == "HP":
            value = (self.individual_values[stat] + self.species.base_stats[stat] + math.sqrt(self.effort_values[stat]) / 8 + 50) * self.level / 50 + 10
        else:
            value = (self.individual_values[stat] + self.species.base_stats[stat] + math.sqrt(self.effort_values[stat]) / 8) * self.level / 50 + 5
            
        return int(value)
        
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
        
        return int(xp)
        
class Player():

    def __init__(self, name, creatures):
        self.name = name
        self.creatures = creatures
        
class GameData():
        
    def __init__(self):
        self.is_in_battle = True
        self.battle_data = BattleData(self, None, None, None)
        
class BattleData():

    def __init__(self, game_data, player_creature, trainer_creature=None, wild_creature=None):
        self.game_data = game_data
        self.player_creature = player_creature
        self.wild_creature = wild_creature
        self.trainer_creature = trainer_creature

    def defending_creature(self):
        return self.trainer_creature if self.trainer_creature != None else self.wild_creature