from map_renderer import *

# Move this to the database eventually?
LOCATION_AREA_MAP_DICT = {}

def create_map(location_area_id, tiles):
    LOCATION_AREA_MAP_DICT[location_area_id] = tiles

def map_from_location_area_id(location_area_id):
    return LOCATION_AREA_MAP_DICT[location_area_id]