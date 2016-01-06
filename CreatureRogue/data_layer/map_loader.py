import sqlite3 as sqlite
from typing import Sequence, Mapping

from CreatureRogue.data_layer.region import Region
from CreatureRogue.data_layer.map_data_tile_type import MapDataTileType


class MapDataTile:
    """
    Represents a single tile in a map.
    """
    def __init__(self, tile_type: MapDataTileType, row: int, column: int):
        self.tile_type = tile_type
        self.row = row
        self.column = column

    @property
    def color(self):
        return self.tile_type.color

    @property
    def display_character(self):
        return self.tile_type.display_character

    def __str__(self):
        return "{0} ({1}, {2})".format(self.tile_type, self.row, self.column)


class MapData:
    """
    Contains the full information on the map for a region.

    TODO - How do we codify the links between different parts of a region?
    """
    def __init__(self, region: Region, tiles: Sequence[Sequence[MapDataTile]]):
        self.region = region
        self.tiles = tiles


class MapLoader:

    def __init__(self, db_file):
        self.db_file = db_file

    def load_map(self, region: Region, tile_types: Mapping[int, MapDataTileType], default_tile_type: MapDataTileType) -> MapData:
        """
        This function will load the data for a given region.

        Loading maps is done separately from the main static data since it
        could theoretically take enough time to slow the application down
        (if there were a lot of regions).

        :param region: The region which we want the data for.
        :param tile_types: The tile types that were loaded as part of the
        static data.
        :param default_tile_type: If a tile doesn't exist in the database
        then this is the type which is loaded in it's place.

        :return: A MapData object containing the full information required to
        render the map.
        """
        with sqlite.connect(self.db_file) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(row) + 1, MAX(\"column\") + 1 FROM region_map_data WHERE region_id = {0}".format(region.id))
            max_row, max_col = cur.fetchone()
            tiles = [[MapDataTile(tile_type=default_tile_type, row=y, column=x) for x in range(max_col)] for y in range(max_row)]

            cur.execute("SELECT row, \"column\", cell_type_id FROM region_map_data WHERE region_id = {0} ORDER BY row, \"column\"".format(region.id))
            for y, x, tile_type_id in cur.fetchall():
                tiles[y][x].tile_type = tile_types[tile_type_id] if tile_type_id in tile_types else default_tile_type

            return MapData(region=region, tiles=tiles)
