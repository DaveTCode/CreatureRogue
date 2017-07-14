from CreatureRogue.data_layer.encounter import Encounter
from CreatureRogue.data_layer.location_area import LocationArea
from CreatureRogue.data_layer.location import Location
from CreatureRogue.data_layer.region import Region
from tests.data_layer.species_test import create_blank_species


def test_str_no_name():
    """
    A location area with no name should have a valid str function.
    """
    l = LocationArea(identifier="", name="", location=Location(identifier="", name="", region=Region(region_id=1, identifier="", name="")), walk_encounters=[])
    assert "" == str(l)


def test_str_name():
    """
    A location area with a name should have a valid str function that
    matches the name.
    """
    l = LocationArea(identifier="", name="test", location=Location(identifier="", name="", region=Region(region_id=1, identifier="", name="")), walk_encounters=[])
    assert "test" == str(l)


def test_no_encounter_if_none_exist():
    """
    No encounter should be returned if there are none valid for this area.
    """
    l = LocationArea(identifier="", name="test", location=Location(identifier="", name="", region=Region(region_id=1, identifier="", name="")), walk_encounters=[])
    assert l.get_encounter() is None


def test_encounter_returned_if_one_exists():
    """
    If only one encounter exists then requesting an encounter from a location area should return it.
    """
    l = LocationArea(identifier="", name="test", location=Location(identifier="", name="", region=Region(region_id=1, identifier="", name="")),
                     walk_encounters=[Encounter(species=create_blank_species("test"), min_level=0, max_level=100, rarity=100)])
    assert l.get_encounter() is not None


def test_encounter_returned_if_multiple_exist():
    """
    If only one encounter exists then requesting an encounter from a location area should return it.
    """
    l = LocationArea(identifier="", name="test", location=Location(identifier="", name="", region=Region(region_id=1, identifier="", name="")),
                     walk_encounters=[Encounter(species=create_blank_species("test"), min_level=0, max_level=100, rarity=70),
                                      Encounter(species=create_blank_species("test2"), min_level=0, max_level=100, rarity=60)])
    assert l.get_encounter() is not None
