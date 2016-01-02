import unittest

from CreatureRogue.data_layer.color import Color
from CreatureRogue.data_layer.growth_rate import GrowthRate
from CreatureRogue.data_layer.species import Species


class SpeciesTests(unittest.TestCase):
    @staticmethod
    def create_blank_species(name: str) -> Species:
        return Species(pokedex_number=1, name=name, height=0, weight=0, types=[], base_stats=[], base_xp_yield=0, growth_rate=GrowthRate("None"),
                       display_character="A", display_color=Color("red", 255, 0, 0), level_moves={}, flavor_text="None", genus="None", capture_rate=0)

    def test_imperial_weight_str_zero_weight(self):
        s = self.create_blank_species("test")
        self.assertEqual("0.0 lbs.", s.imperial_weight_str())

    def test_imperial_weight_str_non_zero_weights(self):
        s = self.create_blank_species("test")
        s.weight = 1
        self.assertEqual("0.2 lbs.", s.imperial_weight_str())
        s.weight = 100
        self.assertEqual("22.0 lbs.", s.imperial_weight_str())
        s.weight = 200
        self.assertEqual("44.1 lbs.", s.imperial_weight_str())

    def test_imperial_height_str_zero_height(self):
        s = self.create_blank_species("test")
        self.assertEqual("0'00\"", s.imperial_height_str())

    def test_imperial_height_str_non_zero_heights(self):
        s = self.create_blank_species("test")
        s.height = 10
        self.assertEqual("3'03\"", s.imperial_height_str())

    def test_zigzagoon_height_weight(self):
        """
        Simple test that a Zigzagoon has exactly the height and weight
        strings that are displayed in pokemon X/Y.
        """
        s = self.create_blank_species("Zigzagoon")
        s.weight = 175
        s.height = 4
        self.assertEqual("38.6 lbs.", s.imperial_weight_str())
        self.assertEqual("1'04\"", s.imperial_height_str())
