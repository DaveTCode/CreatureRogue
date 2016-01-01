import functools
import random


class LocationArea:
    def __init__(self, identifier, name, location, walk_encounters, walk_encounter_rate):
        self.location = location
        self.identifier = identifier
        self.name = name
        self.walk_encounters = walk_encounters
        self.walk_encounter_rate = walk_encounter_rate

    def get_encounter(self):
        """
            Select between all of the available encounters in the location area.

            This is a weighted random selection and can return None if there were
            no encounters available.
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