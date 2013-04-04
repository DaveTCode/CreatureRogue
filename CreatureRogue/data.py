'''
    The static data which constitutes the game is loaded into objects stored 
    in this module.
'''
from __future__ import division
import random

HP_STAT = 1
ATTACK_STAT = 2
DEFENSE_STAT = 3
SP_ATTACK_STAT = 4
SP_DEFENSE_STAT = 5
SPEED_STAT = 6
ACCURACY_STAT = 7
EVASION_STAT = 8

def load_location_area_rects(rects_file_name):
    '''
        Will probably move this elsewhere at some point.
    '''
    rects = LocationAreaRectCollection()
    with open(rects_file_name) as rects_file:
        for line in rects_file:
            location_area_id, x1, y1, x2, y2 = [int(part) for part in line.strip().split(',')]
            rects.add_location_area_rect(LocationAreaRect(location_area_id, x1, y1, x2, y2))

    return rects

class StaticGameData():
    def __init__(self, species, types, type_chart, moves, stats, colors, growth_rates, move_targets, regions, locations, location_areas, xp_lookup, pokeballs):
        self.species = species
        self.types = types
        self.type_chart = type_chart
        self.moves = moves
        self.stats = stats
        self.colors = colors
        self.growth_rates = growth_rates
        self.move_targets = move_targets
        self.regions = regions
        self.locations = locations
        self.location_areas = location_areas
        self.xp_lookup = xp_lookup
        self.pokeballs = pokeballs
        
    def stat(self, stat):
        return self.stats[stat]
        
class LocationAreaRectCollection():
    '''
        This exists as a separate collection so that we could speed up 
        searching by location using better data structures if required.

        To facilitate this all access must be through accessor functions
        not to data directly.
    '''

    def __init__(self):
        self.by_id = {}

    def add_location_area_rect(self, rect):
        '''
            Adds a new location rectangle to the object, will overwrite any 
            existing that uses the same location area id.
        '''
        self.by_id[rect.location_area_id] = rect

    def get_location_area_by_position(self, x, y):
        '''
            Given x,y map coordinates, this function returns the location 
            area which covers those.

            Note, that there is currently nothing policing location area
            overlaps so this will return the first such area.

            If no location area covers these coordinates then returns None.
        '''
        for location_area_id, rect in self.by_id.iteritems():
            if x >= rect.x1 and x <= rect.x2 and y >= rect.y1 and y <= rect.y2:
                return location_area_id

        return None

class LocationAreaRect():
    def __init__(self, location_area_id, x1, y1, x2, y2):
        self.location_area_id = location_area_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return "{0} - ({1},{2}),({3},{4})".format(self.location_area_id, self.x1, self.y1, self.x2, self.y2)

class Stat():
    
    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name
        
    def __str__(self):
        return self.name
        
class Color():
    
    def __init__(self, name, r, g, b):
        self.name = name
        self.r = r
        self.g = g
        self.b = b
        
    def __str__(self):
        return "{0} - ({1},{2},{3})".format(self.name, self.r, self.g, self.b)
        
class GrowthRate():
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return self.name
        
class XpLookup():
    def __init__(self, xp_map):
        self.xp_map = xp_map
        
    def level_at_xp(self, species, xp):
        '''
            The level that a creature is when it has exactly xp amount of 
            experience is determined by the species growth rate and some static
            data which is checked here.
        '''
        level_xps = self.xp_map[species.growth_rate]
        
        for level, level_xp in level_xps.iteritems():
            if xp < level_xp:
                return level

        return 0
        
class Species():
    
    def __init__(self, pokedex_number, name, height, weight, types, base_stats, base_xp_yield, growth_rate, display_character, display_color, level_moves, flavor_text, genus):
        self.pokedex_number = pokedex_number
        self.name = name
        self.height = height
        self.weight = weight
        self.types = types
        self.base_stats = base_stats
        self.base_xp_yield = base_xp_yield
        self.growth_rate = growth_rate
        self.display_character = display_character
        self.display_color = display_color
        self.level_moves = level_moves
        self.flavor_text = flavor_text
        self.genus = genus
        
    def imperial_weight_str(self):
        '''
            Weight is stored in 1/10kg so this function is used to convert to
            an appropriate imperial viewing string of lbs.
        '''
        return '{0:.1f} lbs.'.format(self.weight / 10 * 2.20462)
        
    def imperial_height_str(self):
        '''
            Height is stored in 1/10m in the database so this function is used
            to convert into an imperial display format of feet and inches.
        '''
        feet = self.height / 10 * 3.2808399
        inches = (feet % 1) * 12
        
        return '{0}\'{1:0=2d}"'.format(int(feet), int(round(inches)))
        
    def move_data_at_level(self, level):
        '''
            When a wild creature is encountered, it's move set is the most 
            recent 4 moves that it would have learnt from leveling up.
            
            This function calculates that set of moves (may be less than 4).
        '''
        moves = []
        for i in range(level, 0, -1):
            moves = moves + self.level_moves[i]
            
            if len(moves) >= 4:
                break
                
        return moves[:4]
        
    def level(self, xp_loader, current_xp):
        '''
            The level of a species is determined solely by its current xp.
        '''
        return xp_loader.level_at_xp(self, current_xp)
    
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
        type_chart_str = ""
    
        for attacking_type in self.chart:
            type_chart_str = str(attacking_type) + " - "

            type_chart_str += ",".join(["({0}:{1}), ".format(defending_type, self.chart[attacking_type][defending_type]) for defending_type in self.chart[attacking_type]]) + "\n"
        
        return type_chart_str
        
class MoveTarget():
    
    def __init__(self, identifier, name, description):
        self.identifier = identifier
        self.name = name
        self.description = description
        
class MoveData():
    
    def __init__(self, name, max_pp, type, base_attack, base_accuracy, min_hits, max_hits, stat_changes, attack_stat, defence_stat, accuracy_stat, evasion_stat, target):
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
        self.target = target
    
    def damage_move(self):
        '''
            Determines whether a move affects the targets health.
        '''
        return not self.attack_stat == None
        
    def stat_change_move(self):
        '''
            Determines whether a move affects the targets stats. This is 
            independent of whether it affects their health.
        '''
        for stat in self.stat_changes:
            if self.stat_changes[stat] != 0:
                return True
                
        return False
    
    def __str__(self):
        return self.name
        
class Region():

    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name
        
    def __str__(self):
        return self.name
        
class Location():

    def __init__(self, identifier, name, region):
        self.region = region
        self.identifier = identifier
        self.name = name
        
    def __str__(self):
        return self.name
        
class LocationArea():

    def __init__(self, identifier, name, location, walk_encounters, walk_encounter_rate):
        self.location = location
        self.identifier = identifier
        self.name = name
        self.walk_encounters = walk_encounters
        self.walk_encounter_rate = walk_encounter_rate
        
    def get_encounter(self):
        '''
            Select between all of the available encounters in the location area.

            This is a weighted random selection and can return None if there were
            no encounters available.
        '''
        total_rarity = reduce(lambda x, y: x + y.rarity, self.walk_encounters, 0)
        rand = random.randint(0, total_rarity if total_rarity == 0 else total_rarity - 1)

        total = 0
        for encounter in self.walk_encounters:
            total += encounter.rarity
            if total > rand:
                return encounter

        return None

    def __str__(self):
        return self.name

class Encounter():

    def __init__(self, species, min_level, max_level, rarity):
        self.species = species
        self.min_level = min_level
        self.max_level = max_level
        self.rarity = rarity

    def __str__(self):
        return "Encounter: {0} ({1},{2})".format(str(self.species), self.min_level, self.max_level)

class Pokeball():

    def __init__(self, pokeball_id, name, catch_rate, top_color, bottom_color):
        self.pokeball_id = pokeball_id
        self.name = name
        self.catch_rate = catch_rate
        self.top_color = top_color
        self.bottom_color = bottom_color

    def __str__(self):
        return self.name