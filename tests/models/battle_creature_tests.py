import unittest
from CreatureRogue.models.creature import Creature
from CreatureRogue.models.battle_creature import BattleCreature
from CreatureRogue.data_layer.data import StaticGameData


class BattleCreatureTests(unittest.TestCase):
    def testStringBlankName(self):
        c = BattleCreature(creature=Creature(), static_game_data=StaticGameData())
        self.assertEqual("", str(a))
