from CreatureRogue.data_layer.species import Species


class Encounter:
    def __init__(self, species: Species, min_level: int, max_level: int, rarity):
        self.species = species
        self.min_level = min_level
        self.max_level = max_level
        self.rarity = rarity

    def __str__(self):
        return "Encounter: {0} ({1},{2})".format(self.species, self.min_level, self.max_level)
