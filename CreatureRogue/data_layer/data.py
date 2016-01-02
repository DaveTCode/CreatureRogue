"""
    The static data which constitutes the game is loaded into objects stored 
    in this module.
"""
from CreatureRogue.data_layer.location_area_rect import LocationAreaRect
from CreatureRogue.data_layer.location_area_rect_collection import LocationAreaRectCollection

# TODO - Change to enum?
HP_STAT = 1
ATTACK_STAT = 2
DEFENSE_STAT = 3
SP_ATTACK_STAT = 4
SP_DEFENSE_STAT = 5
SPEED_STAT = 6
ACCURACY_STAT = 7
EVASION_STAT = 8


def load_location_area_rects(rects_file_name):
    """
        TODO - Put somewhere sensible
    """
    rects = LocationAreaRectCollection()
    with open(rects_file_name) as rects_file:
        for line in rects_file:
            location_area_id, x1, y1, x2, y2 = [int(part) for part in line.strip().split(',')]
            rects.add_location_area_rect(LocationAreaRect(location_area_id, x1, y1, x2, y2))

    return rects


class StaticGameData:
    def __init__(self, species, types, type_chart, moves, stats, colors, growth_rates, move_targets, regions, locations, location_areas, xp_lookup, pokeballs, ailments):
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
        self.ailments = ailments
        
    def stat(self, stat):
        return self.stats[stat]

