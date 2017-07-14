import pytest
from CreatureRogue.data_layer.color import Color
from CreatureRogue.data_layer.growth_rate import GrowthRate
from CreatureRogue.data_layer.species import Species
from tests.data_layer.move_data_test import create_default_move_data


def create_blank_species(name: str) -> Species:
    return Species(pokedex_number=1, name=name, height=0, weight=0, types=[], base_stats=[], base_xp_yield=0,
                   growth_rate=GrowthRate("None"), display_character="A", display_color=Color("red", 255, 0, 0),
                   level_moves={}, flavor_text="None", genus="None", capture_rate=0)


def test_imperial_weight_str_zero_weight():
    """
    Zero weight returns a sensible weight string.
    :return:
    """
    s = create_blank_species("test")
    assert "0.0 lbs." == s.imperial_weight_str()


def test_imperial_weight_str_non_zero_weights():
    """
    Non zero weights return the correct weight strings.
    """
    s = create_blank_species("test")
    s.weight = 1
    assert "0.2 lbs." == s.imperial_weight_str()
    s.weight = 100
    assert "22.0 lbs." == s.imperial_weight_str()
    s.weight = 200
    assert "44.1 lbs." == s.imperial_weight_str()


def test_imperial_height_str_zero_height():
    """
    Zero height still returns a valid string.
    """
    s = create_blank_species("test")
    assert "0'00\"" == s.imperial_height_str()


def test_imperial_height_str_non_zero_heights():
    """
    Non zero heights return valid imperial height strings.
    """
    s = create_blank_species("test")
    s.height = 10
    assert "3'03\"" == s.imperial_height_str()


def test_zigzagoon_height_weight():
    """
    Simple test that a Zigzagoon has exactly the height and weight
    strings that are displayed in pokemon X/Y.
    """
    s = create_blank_species("Zigzagoon")
    s.weight = 175
    s.height = 4
    assert "38.6 lbs." == s.imperial_weight_str()
    assert "1'04\"" == s.imperial_height_str()


def test_string_blank_name():
    s = create_blank_species("")
    assert "" == str(s)


def test_string_non_blank_name():
    s = create_blank_species("Zigzagoon")
    assert "Zigzagoon" == str(s)


def test_string_non_ascii_name():
    s = create_blank_species("Porygon-Z")
    assert "Porygon-Z" == str(s)
    s = create_blank_species("Farfetch'd")
    assert "Farfetch'd" == str(s)


def test_move_data_assert_on_bad_level():
    s = create_blank_species("")
    with pytest.raises(AssertionError):
        s.move_data_at_level(0)


def test_move_data_no_moves():
    s = create_blank_species("")
    moves = s.move_data_at_level(1)
    assert 0 == len(moves)


def test_move_data_one_move():
    s = create_blank_species("")
    s.level_moves = {1: [create_default_move_data("")]}
    moves = s.move_data_at_level(1)
    assert 1 == len(moves)
    assert "" == moves[0].name


def test_move_data_four_moves_one_level():
    s = create_blank_species("")
    s.level_moves = {1: [create_default_move_data("1"), create_default_move_data("2"),
                         create_default_move_data("3"), create_default_move_data("4")]}
    moves = s.move_data_at_level(1)
    assert 4 == len(moves)
    assert "1" == moves[0].name
    assert "2" == moves[1].name
    assert "3" == moves[2].name
    assert "4" == moves[3].name


def test_move_data_four_moves_four_levels():
    s = create_blank_species("")
    s.level_moves = {1: [create_default_move_data("1")],
                     2: [create_default_move_data("2")],
                     3: [create_default_move_data("3")],
                     4: [create_default_move_data("4")]}
    moves = s.move_data_at_level(4)
    assert 4 == len(moves)
    assert "4" == moves[0].name
    assert "3" == moves[1].name
    assert "2" == moves[2].name
    assert "1" == moves[3].name


def test_move_data_discard_move():
    s = create_blank_species("")
    s.level_moves = {1: [create_default_move_data("1")],
                     2: [create_default_move_data("2")],
                     3: [create_default_move_data("3")],
                     4: [create_default_move_data("4")],
                     5: [create_default_move_data("5")]}
    moves = s.move_data_at_level(5)
    assert 4 == len(moves)
    assert "5" == moves[0].name
    assert "4" == moves[1].name
    assert "3" == moves[2].name
    assert "2" == moves[3].name
