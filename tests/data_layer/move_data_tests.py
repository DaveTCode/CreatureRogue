import unittest

from CreatureRogue.data_layer.ailment import Ailment
from CreatureRogue.data_layer.move_data import MoveData
from CreatureRogue.data_layer.move_target import MoveTarget
from CreatureRogue.data_layer.stat import Stat
from CreatureRogue.data_layer.type import Type


class MoveDataTests(unittest.TestCase):
    @staticmethod
    def create_default(name: str) -> MoveData:
        return MoveData(name=name, max_pp=0, type=Type(name="None"), base_attack=0, base_accuracy=0,
                        min_hits=0, max_hits=0, stat_changes={}, attack_stat=None, defence_stat=None,
                        accuracy_stat=None, evasion_stat=None, target=MoveTarget("None", "None", "None"),
                        ailment=Ailment(ailment_id=0, name="None"))

    def test_is_attack_move_true(self):
        m = self.create_default("")
        m.attack_stat = Stat(name="stat", short_name="st")
        self.assertTrue(m.damage_move())

    def test_is_attack_move_false(self):
        m = self.create_default("")
        m.attack_stat = None
        self.assertFalse(m.damage_move())

    def test_is_stat_change_move_true_single_stat(self):
        m = self.create_default("")
        m.stat_changes[Stat(name="stat", short_name="st")] = 1
        self.assertTrue(m.stat_change_move())

    def test_is_stat_change_move_true_multiple_stats(self):
        m = self.create_default("")
        m.stat_changes[Stat(name="stat", short_name="st")] = 0
        m.stat_changes[Stat(name="stat2", short_name="st2")] = 1
        self.assertTrue(m.stat_change_move())

    def test_is_stat_change_move_false_no_stats(self):
        m = self.create_default("")
        self.assertFalse(m.stat_change_move())

    def test_is_stat_change_move_false_one_stat(self):
        m = self.create_default("")
        m.stat_changes[Stat(name="stat", short_name="st")] = 0
        self.assertFalse(m.stat_change_move())

    def test_is_stat_change_move_false_multiple_moves(self):
        m = self.create_default("")
        m.stat_changes[Stat(name="stat", short_name="st")] = 0
        m.stat_changes[Stat(name="stat2", short_name="st2")] = 0
        self.assertFalse(m.stat_change_move())

    def test_str(self):
        m = self.create_default("")
        self.assertEqual("", str(m))

    def test_str_real_name(self):
        m = self.create_default("Pound")
        self.assertEqual("Pound", str(m))
