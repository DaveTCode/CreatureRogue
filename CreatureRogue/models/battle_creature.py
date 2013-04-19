'''
    When in battle a creature can have stat adjustments and other values
    can be modified.

    The battle creature is an encapsulating object which is used to capture 
    this information in an easily discardable manner.
'''
from __future__ import division

class BattleCreature():
    stat_adjust_factors = {-6: 1/4, -5: 2/7, -4: 1/3, -3: 2/5, -2: 1/2, -1: 2/3, 
                           0: 1.0, 
                           1: 1.5, 2: 2.0, 3: 2.5, 4: 3.0, 5: 3.5, 6: 4.0}

    def __init__(self, creature, static_game_data):
        self.static_game_data = static_game_data
        self.creature = creature
        self.stat_adjusts = {stat: 0 for stat in self.creature.stats}
        
    def adjust_stat_adjusts(self, stat, value):
        '''
            The only adjustment to statistics of a creature in battle is done 
            through these factors which range from -6 to 6.
            
            Returns the amount by which we actually adjusted the stat.
        '''
        old_val = self.stat_adjusts[stat]
        self.stat_adjusts[stat] += value
        
        self.stat_adjusts[stat] = max(-6, min(6, self.stat_adjusts[stat]))
            
        return self.stat_adjusts[stat] - old_val
        
    def stat_value(self, stat):
        '''
            The current value of a stat in battle is the base stat for that 
            creature (i.e. the value pre battle) multiplied by the factor
            gained from moves performed on the creature during battle.
            
            These factors are fixed and are capped at 1/4 to 4.
        '''
        return self.creature.stats[stat] * BattleCreature.stat_adjust_factors[self.stat_adjusts[stat]]

    def modified_catch_rate(self, pokeball):
        '''
            Calculates the modified catch rate of a creature. This is based on
            a variety of factors including the status of the creature, the ball
            used and the current hit points.

            It is calculated in BattleCreature rather than Creature because it
            is only applicable during a battle.
        '''
        # TODO - Add status effects
        hp_stat = self.static_game_data.stats[data.HP_STAT]
        triple_max_hp = 3 * self.creature.max_stat(hp_stat)
        return (triple_max_hp - 2 * self.stat_value(hp_stat)) * self.creature.species.capture_rate * pokeball.catch_rate / triple_max_hp