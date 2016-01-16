import unittest

from CreatureRogue.data_layer.color import Color
from CreatureRogue.data_layer.growth_rate import GrowthRate
from CreatureRogue.data_layer.species import Species
from tests.data_layer.move_data_tests import MoveDataTests


class SpeciesTests(unittest.TestCase):
    @staticmethod
    def create_blank_species(name: str) -> Species:
        return Species(pokedex_number=1, name=name, height=0, weight=0, types=[], base_stats=[], base_xp_yield=0, growth_rate=GrowthRate("None"),
                       display_character="A", display_color=Color("red", 255, 0, 0), level_moves={}, flavor_text="None", genus="None", capture_rate=0)

    def test_imperial_weight_str_zero_weight(self):
        """
        Zero weight returns a sensible weight string.
        :return:
        """
        s = self.create_blank_species("test")
        self.assertEqual("0.0 lbs.", s.imperial_weight_str())

    def test_imperial_weight_str_non_zero_weights(self):
        """
        Non zero weights return the correct weight strings.
        """
        s = self.create_blank_species("test")
        s.weight = 1
        self.assertEqual("0.2 lbs.", s.imperial_weight_str())
        s.weight = 100
        self.assertEqual("22.0 lbs.", s.imperial_weight_str())
        s.weight = 200
        self.assertEqual("44.1 lbs.", s.imperial_weight_str())

    def test_imperial_height_str_zero_height(self):
        """
        Zero height still returns a valid string.
        """
        s = self.create_blank_species("test")
        self.assertEqual("0'00\"", s.imperial_height_str())

    def test_imperial_height_str_non_zero_heights(self):
        """
        Non zero heights return valid imperial height strings.
        """
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

    def test_string_blank_name(self):
        s = self.create_blank_species("")
        self.assertEqual("", str(s))

    def test_string_non_blank_name(self):
        s = self.create_blank_species("Zigzagoon")
        self.assertEqual("Zigzagoon", str(s))

    def test_string_non_ascii_name(self):
        s = self.create_blank_species("Porygon-Z")
        self.assertEqual("Porygon-Z", str(s))
        s = self.create_blank_species("Farfetch'd")
        self.assertEqual("Farfetch'd", str(s))

    def test_move_data_assert_on_bad_level(self):
        s = self.create_blank_species("")
        with self.assertRaises(AssertionError):
            s.move_data_at_level(0)

    def test_move_data_no_moves(self):
        s = self.create_blank_species("")
        moves = s.move_data_at_level(1)
        self.assertListEqual([], moves)

    def test_move_data_one_move(self):
        s = self.create_blank_species("")
        s.level_moves = {1: [MoveDataTests.create_default("")]}
        moves = s.move_data_at_level(1)
        self.assertEqual(1, len(moves))
        self.assertEqual("", moves[0].name)

    def test_move_data_four_moves_one_level(self):
        s = self.create_blank_species("")
        s.level_moves = {1: [MoveDataTests.create_default("1"), MoveDataTests.create_default("2"),
                             MoveDataTests.create_default("3"), MoveDataTests.create_default("4")]}
        moves = s.move_data_at_level(1)
        self.assertEqual(4, len(moves))
        self.assertEqual("1", moves[0].name)
        self.assertEqual("2", moves[1].name)
        self.assertEqual("3", moves[2].name)
        self.assertEqual("4", moves[3].name)

    def test_move_data_four_moves_four_levels(self):
        s = self.create_blank_species("")
        s.level_moves = {1: [MoveDataTests.create_default("1")],
                         2: [MoveDataTests.create_default("2")],
                         3: [MoveDataTests.create_default("3")],
                         4: [MoveDataTests.create_default("4")]}
        moves = s.move_data_at_level(4)
        self.assertEqual(4, len(moves))
        self.assertEqual("4", moves[0].name)
        self.assertEqual("3", moves[1].name)
        self.assertEqual("2", moves[2].name)
        self.assertEqual("1", moves[3].name)

    def test_move_data_discard_move(self):
        s = self.create_blank_species("")
        s.level_moves = {1: [MoveDataTests.create_default("1")],
                         2: [MoveDataTests.create_default("2")],
                         3: [MoveDataTests.create_default("3")],
                         4: [MoveDataTests.create_default("4")],
                         5: [MoveDataTests.create_default("5")]}
        moves = s.move_data_at_level(5)
        self.assertEqual(4, len(moves))
        self.assertEqual("5", moves[0].name)
        self.assertEqual("4", moves[1].name)
        self.assertEqual("3", moves[2].name)
        self.assertEqual("2", moves[3].name)
