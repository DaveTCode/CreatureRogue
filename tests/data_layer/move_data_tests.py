import unittest

from CreatureRogue.data_layer.ailment import Ailment
from CreatureRogue.data_layer.move_data import MoveData
from CreatureRogue.data_layer.type import Type
from CreatureRogue.data_layer.move_target import MoveTarget


class MoveDataTests(unittest.TestCase):
    @staticmethod
    def create_default(name: str) -> MoveData:
        return MoveData(name=name, max_pp=0, type=Type(name="None"), base_attack=0, base_accuracy=0,
                        min_hits=0, max_hits=0, stat_changes={}, attack_stat=None, defence_stat=None,
                        accuracy_stat=None, evasion_stat=None, target=MoveTarget("None", "None", "None"),
                        ailment=Ailment(ailment_id=0, name="None"))
