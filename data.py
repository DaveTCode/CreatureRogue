from __future__ import division
import random
import math

class StaticGameData():
    def __init__(self, species, types, type_chart, moves, stats, colors, growth_rates):
        self.species = species
        self.types = types
        self.type_chart = type_chart
        self.moves = moves
        self.stats = stats
        self.colors = colors
        self.growth_rates = growth_rates
        
    def hp_stat(self):
        return self.stats[1]
        
    def accuracy_stat(self):
        return self.stats[7]
        
    def evasion_stat(self):
        return self.stats[8]
        
class Stat():
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
        
class Color():
    
    def __init__(self, name, r, g, b):
        self.name = name
        self.r = r
        self.g = g
        self.b = b
        
    def __str__(self):
        return self.name + "(" + str(self.r) + "," + str(self.g) + "," + str(self.b) + ")"
        
class GrowthRate():
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
        
class XpLookup():
    def __init__(self, map):
        self.map = map
        
    def level_at_xp(species, xp):
        level_xps = self.map[species.growth_rate]
        
        prev_xp = 0
        for level_xp in level_xps:
            if xp > prev_xp and xp < level_xp[1]:
                return level_xp[0]
            
            prev_xp = level_xp[1]
        
class Species():
    
    def __init__(self, name, types, base_stats, base_xp_yield, growth_rate, display_character, display_color):
        self.name = name
        self.types = types
        self.base_stats = base_stats
        self.base_xp_yield = base_xp_yield
        self.growth_rate = growth_rate
        self.display_character = display_character
        self.display_color = display_color
        
    def level(self, xp_loader, current_xp):
        '''
            The level of a species is determined solely by its current xp so
            we don't store the data directly.
        '''
        return xp_lookup.level_at_xp(self, current_xp)
    
    def __str__(self):
        return self.name
        
class Type():
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
        
class TypeChart():

    def __init__(self, chart):
        self.chart = chart
        
    def damage_modifier(self, attacking_type, defending_type):
        '''
            The type chart hold information on how attacks of all types affect
            creatures of all types. This function allows us to query that 
            information.
        '''
        if attacking_type in self.chart and defending_type in self.chart[attacking_type]:
            return self.chart[attacking_type][defending_type]
        else:
            return 1
            
    def __str__(self):
        s = ""
    
        for attacking_type in self.chart:
            s = s + str(attacking_type) + " - "
            for defending_type in self.chart[attacking_type]:
                s = s + "(" + str(defending_type) + ":" + str(self.chart[attacking_type][defending_type]) + "),  "
                
            s = s + "\n"
        return s
        
class MoveData():
    
    def __init__(self, name, max_pp, type, base_attack, base_accuracy, min_hits, max_hits, stat_changes, attack_stat, defence_stat, accuracy_stat, evasion_stat):
        self.name = name
        self.max_pp = max_pp
        self.type = type
        self.base_attack = base_attack
        self.base_accuracy = base_accuracy
        self.attack_stat = attack_stat
        self.defence_stat = defence_stat
        self.accuracy_stat = accuracy_stat
        self.evasion_stat = evasion_stat
        self.min_hits = min_hits
        self.max_hits = max_hits
        self.stat_changes = stat_changes
    
    def damage_move(self):
        return not self.attack_stat == None
    
    def __str__(self):
        return self.name