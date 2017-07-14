from CreatureRogue.data_layer.ailment import Ailment
from CreatureRogue.data_layer.move_data import MoveData
from CreatureRogue.data_layer.move_target import MoveTarget
from CreatureRogue.data_layer.stat import Stat
from CreatureRogue.data_layer.type import Type


def create_default_move_data(name: str) -> MoveData:
    return MoveData(name=name, max_pp=0, move_type=Type(name="None"), base_attack=0, base_accuracy=0,
                    min_hits=0, max_hits=0, stat_changes={}, attack_stat=None, defence_stat=None,
                    accuracy_stat=None, evasion_stat=None, target=MoveTarget("None", "None", "None"),
                    ailment=Ailment(ailment_id=0, name="None"))


def test_is_attack_move_true():
    m = create_default_move_data("")
    m.attack_stat = Stat(name="stat", short_name="st")
    assert m.damage_move()


def test_is_attack_move_false():
    m = create_default_move_data("")
    m.attack_stat = None
    assert not m.damage_move()


def test_is_stat_change_move_true_single_stat():
    m = create_default_move_data("")
    m.stat_changes[Stat(name="stat", short_name="st")] = 1
    assert m.stat_change_move()


def test_is_stat_change_move_true_multiple_stats():
    m = create_default_move_data("")
    m.stat_changes[Stat(name="stat", short_name="st")] = 0
    m.stat_changes[Stat(name="stat2", short_name="st2")] = 1
    assert m.stat_change_move()


def test_is_stat_change_move_false_no_stats():
    m = create_default_move_data("")
    assert not m.stat_change_move()


def test_is_stat_change_move_false_one_stat():
    m = create_default_move_data("")
    m.stat_changes[Stat(name="stat", short_name="st")] = 0
    assert not m.stat_change_move()


def test_is_stat_change_move_false_multiple_moves():
    m = create_default_move_data("")
    m.stat_changes[Stat(name="stat", short_name="st")] = 0
    m.stat_changes[Stat(name="stat2", short_name="st2")] = 0
    assert not m.stat_change_move()


def test_str():
    m = create_default_move_data("")
    assert "" == str(m)


def test_str_real_name():
    m = create_default_move_data("Pound")
    assert "Pound" == str(m)
