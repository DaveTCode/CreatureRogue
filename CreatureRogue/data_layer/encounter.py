class Encounter:

    def __init__(self, species, min_level, max_level, rarity):
        self.species = species
        self.min_level = min_level
        self.max_level = max_level
        self.rarity = rarity

    def __str__(self):
        return "Encounter: {0} ({1},{2})".format(str(self.species), self.min_level, self.max_level)