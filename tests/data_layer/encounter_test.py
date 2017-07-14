from CreatureRogue.data_layer.encounter import Encounter
from tests.data_layer.species_test import create_blank_species


def test_string():
    e = Encounter(species=create_blank_species("testing"), min_level=1, max_level=3, rarity=7)
    assert "Encounter: testing (1,3)" == str(e)
