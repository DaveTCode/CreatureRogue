import functools
import random
from collections.abc import Sequence

from CreatureRogue.data_layer.encounter import Encounter
from CreatureRogue.data_layer.location import Location


class LocationArea:
    """
    A location area is the region of the map which contains a certain set of
    encounters.
    """

    def __init__(
        self, identifier: str, name: str, location: Location, walk_encounters: Sequence[Encounter]
    ):
        self.location = location
        self.identifier = identifier
        self.name = name
        self.walk_encounters = walk_encounters  # TODO - Convert walk_encounters to an encounters map that takes an encounter type (id?) and maps to a set of encounters instead

    def get_encounter(self) -> Encounter | None:
        """
        Select between all of the available encounters in the location area.

        This is a weighted random selection and can return None if there were
        no encounters available.

        Note that this is not intended to determine whether an encounter
        should occur, this will always return an encounter if one exists
        for the area.

        TODO - This currently assumes that the encounter type is walking.
        """
        total_rarity = functools.reduce(lambda x, y: x + y.rarity, self.walk_encounters, 0)
        rand = random.randint(0, total_rarity if total_rarity == 0 else total_rarity - 1)

        total = 0
        for encounter in self.walk_encounters:
            total += encounter.rarity
            if total > rand:
                return encounter

        return None

    def __str__(self):
        return self.name
