from maps import *

# Move this to the database eventually?
LOCATION_AREA_MAP_DICT = {285: pallet_town, 295: route_1}

class MapLoader():
    @staticmethod
    def map_from_location_area_id(location_area_id):
        '''
            Given a location area id from the database this returns the list of 
            tiles in rows.

            It will throw a key error if the location area doesn't have a map.
        '''
        return LOCATION_AREA_MAP_DICT[location_area_id].tiles
