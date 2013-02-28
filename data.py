class StaticGameData():
    def __init__(self, species, types, type_chart, moves, stats, colors, growth_rates):
        self.species = species
        self.types = types
        self.type_chart = type_chart
        self.moves = moves
        self.stats = stats
        self.colors = colors
        self.growth_rates = growth_rates
        
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
    
    def __init__(self, name, types, base_hp, base_xp_yield, growth_rate, display_character, display_color):
        self.name = name
        self.types = types
        self.base_hp = base_hp
        self.base_xp_yield = base_xp_yield
        self.growth_rate = growth_rate
        self.display_character = display_character
        self.display_color = display_color
        
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
        
    def damage_modifier(attacking_type, defending_type):
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
            s = str(attacking_type) + " - "
            for defending_type in self.chart[attacking_type]:
                s = s + "(" + str(defending_type) + ":" + str(self.chart[attacking_type][defending_type]) + ")\n"
                
        return s
        
class Move():
    
    def __init__(self, name, max_pp, type):
        self.name = name
        self.max_pp = max_pp
        self.type = type
        
    def __str__(self):
        return self.name
        
class AttackingMove(Move):
    
    def __init__(self, name, max_pp, type, base_attack, attack_stat, defence_stat):
        Move.__init__(self, name, max_pp, type)
        self.base_attack = base_attack
        self.attack_stat = attack_stat
        self.defence_stat = defence_stat
        
    def damage_calculation(self, attacking_creature, defending_creature, type_chart):
        '''
            To calculate the damage that a move does we need to know which
            creature is performing the move and which is defending it.
            
            The return value for this is the hitpoint delta.
        '''
        attack_stat_value = attacking_creature.stats[self.attack_stat]
        defence_stat_value = defending_creature.stats[self.defence_stat]
        
        # Modifiers
        critical_modifier = 2 if random.uniform(0, 100) < 6.25 else 1 # TODO: Incomplete - should use items and check whether this is a high critical move etc
        same_type_attack_bonus = 1.5 if self.type in attacking_creature.types else 1
        type_modifier = 1
        for type in defending_creature.types:
            type_modifier = type_modifier * type_chart.damage_modifier(self.type, type)
            
        modifier = same_type_attack_bonus * type_modifier * critical_modifier # TODO: Incomplete - Ignoring weather effects and other bits
        
        return math.floor((((2 * attacking_creature.level + 10) / 250) * (attack_stat_value / defence_stat_value) * self.base_attack + 2) * modifier)