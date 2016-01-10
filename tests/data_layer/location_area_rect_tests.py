import unittest

from CreatureRogue.data_layer.location_area_rect import LocationAreaRect


class LocationAreaRectTests(unittest.TestCase):
    def test_str_representation(self):
        l = LocationAreaRect(location_area_id=1, x1=100, x2=120, y1=200, y2=220)
        self.assertEqual("1 - (100,200),(120,220)", str(l))
