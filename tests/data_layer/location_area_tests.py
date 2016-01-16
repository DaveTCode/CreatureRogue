import unittest

from CreatureRogue.data_layer.encounter import Encounter
from CreatureRogue.data_layer.location_area import LocationArea
from CreatureRogue.data_layer.location import Location
from CreatureRogue.data_layer.region import Region
from tests.data_layer.species_tests import SpeciesTests


class LocationAreaTests(unittest.TestCase):
    def test_str_no_name(self):
        """
        A location area with no name should have a valid str function.
        """
        l = LocationArea(identifier="", name="", location=Location(identifier="", name="", region=Region(id=1, identifier="", name="")), walk_encounters=[])
        self.assertEqual("", str(l))

    def test_str_name(self):
        """
        A location area with a name should have a valid str function that
        matches the name.
        """
        l = LocationArea(identifier="", name="test", location=Location(identifier="", name="", region=Region(id=1, identifier="", name="")), walk_encounters=[])
        self.assertEqual("test", str(l))

    def test_no_encounter_if_none_exist(self):
        """
        No encounter should be returned if there are none valid for this area.
        """
        l = LocationArea(identifier="", name="test", location=Location(identifier="", name="", region=Region(id=1, identifier="", name="")), walk_encounters=[])
        self.assertIsNone(l.get_encounter())

    def test_encounter_returned_if_one_exists(self):
        """
        If only one encounter exists then requesting an encounter from a location area should return it.
        """
        l = LocationArea(identifier="", name="test", location=Location(identifier="", name="", region=Region(id=1, identifier="", name="")),
                         walk_encounters=[Encounter(species=SpeciesTests.create_blank_species("test"), min_level=0, max_level=100, rarity=100)])
        self.assertIsNotNone(l.get_encounter())

    def test_encounter_returned_if_multiple_exist(self):
        """
        If only one encounter exists then requesting an encounter from a location area should return it.
        """
        l = LocationArea(identifier="", name="test", location=Location(identifier="", name="", region=Region(id=1, identifier="", name="")),
                         walk_encounters=[Encounter(species=SpeciesTests.create_blank_species("test"), min_level=0, max_level=100, rarity=70),
                                          Encounter(species=SpeciesTests.create_blank_species("test2"), min_level=0, max_level=100, rarity=60)])
        self.assertIsNotNone(l.get_encounter())
