import unittest

from CreatureRogue.data_layer.encounter import Encounter
from tests.data_layer.species_tests import SpeciesTests


class EncounterTests(unittest.TestCase):
    def testString(self):
        e = Encounter(species=SpeciesTests.create_blank_species("testing"), min_level=1, max_level=3, rarity=7)
        self.assertEqual("Encounter: testing (1,3)", str(e))
