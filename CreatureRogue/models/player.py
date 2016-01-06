"""
    The player is the object which contains all specific information to the
    actual user.

    It is only used for the human player and not for trainers.
"""
import random

from CreatureRogue.data_layer.data import StaticGameData
from CreatureRogue.data_layer.map_loader import MapData, MapDataTile
from CreatureRogue.data_layer.pokeball import Pokeball
from CreatureRogue.models.creature import Creature
from CreatureRogue.renderer import map_renderer


class Player:

    def __init__(self, name: str, static_game_data: StaticGameData, map_data: MapData, x: int, y: int):
        self.name = name
        self.creatures = []
        self.pokedex = {static_game_data.species[species_id].pokedex_number: (0, static_game_data.species[species_id]) for species_id in static_game_data.species}
        self.map_data = map_data
        self.coords = (x, y)
        self.steps_in_long_grass_since_encounter = 0
        self.static_game_data = static_game_data
        self.pokeballs = {static_game_data.pokeballs[pokeball_id]: 0 for pokeball_id in static_game_data.pokeballs}
        
    def available_pokeballs(self):
        """
            Checks whether the player has any available pokeballs.
        """
        return {pokeball: self.pokeballs[pokeball] for pokeball in self.pokeballs if self.pokeballs[pokeball] > 0}

    def use_pokeball(self, pokeball: Pokeball):
        """
            Called when the player uses up a pokeball.
        """
        self.pokeballs[pokeball] = max(0, self.pokeballs[pokeball] - 1)

    def get_location_area(self):
        """
            The location area of a player is determined by the x, y coordinates 
            and the static game data.
        """
        x, y = self.coords
        location_area_id = self.static_game_data.location_area_rects.get_location_area_by_position(x, y)  # TODO - No location_area_rects on static game data object.

        if location_area_id is not None:
            return self.static_game_data.location_areas[location_area_id]

        return None

    def _can_traverse(self, cell: MapDataTile):
        """
            Depending on the current player state they may or may not be able 
            to traverse any given cell. This check is made every time the 
            player attempts to move onto a new cell.

            Returns true if the player is allowed to travel on that cell and
            false otherwise.
        """
        # TODO - Only really check that the cell is always traversable at the moment
        return cell.tile_type.traversable

    def _causes_encounter(self):
        """
            Calculation used to determine whether a player causes an encounter 
            with movement.

            It is called each time the player steps on a square that could 
            cause an encounter and returns true if an encounter should be 
            generated and false otherwise.
        """
        location_area = self.get_location_area()
        encounter_rate = min(100, location_area.walk_encounter_rate)

        if 8 - encounter_rate // 10 < self.steps_in_long_grass_since_encounter:
            if random.random() < 0.95:
                return False

        if random.randint(0, 99) < encounter_rate and random.randint(0, 99) < 40:
            return True
        else:
            return False

    def move_to_cell(self, x: int, y: int):
        """
            Move to the cell specified by x,y in the current map.

            Returns (whether moved, whether caused a wild encounter)
        """
        if self._can_traverse(self.map_data.tiles[y][x]):
            self.coords = (x, y)
            causes_encounter = False

            if self.get_cell().base_cell == map_renderer.LONG_GRASS:
                self.steps_in_long_grass_since_encounter += 1

                causes_encounter = self._causes_encounter()
            else:
                self.steps_in_long_grass_since_encounter = 0

            return True, causes_encounter
        else:
            return False, False

    def get_cell(self):
        """
            Returns the exact cell that the player is currently on.
        """
        return self.map_data.tiles[self.coords[1]][self.coords[0]]

    def encounter_creature(self, creature: Creature):
        """
            Called whenever a creature is encountered (even it it isn't new).

            Is responsible for updating the pokedex.
        """
        self.pokedex[creature.species.pokedex_number] = (1, creature.species)

    def catch_creature(self, creature: Creature):
        """
            Called whenever a creature is caught in the wild.

            Is responsible for updating the pokedex.
        """
        self.pokedex[creature.species.pokedex_number] = (2, creature.species)