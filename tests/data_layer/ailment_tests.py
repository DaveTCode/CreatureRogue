import unittest
from CreatureRogue.data_layer.ailment import Ailment


class AilmentTests(unittest.TestCase):
    def testStringBlankName(self):
        a = Ailment(0, "")
        self.assertEqual("", str(a))

    def testStringRealName(self):
        a = Ailment(0, "Hello I'm a name")
        self.assertEqual("Hello I'm a name", str(a))
