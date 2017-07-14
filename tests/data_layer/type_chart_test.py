from CreatureRogue.data_layer.type import Type
from CreatureRogue.data_layer.type_chart import TypeChart


def test_empty_type_chart():
    """
    Check that an empty type chart has a sensible str representation and
    that accessing elements in it doesn't cause exceptions to be thrown.
    """
    type_chart = TypeChart({})
    assert "" == str(type_chart)
    assert 100 == type_chart.damage_modifier(Type("test"), Type("test2"))


def test_single_entry_type_chart():
    """
    Check that a type chart with only one entry has a sensible string
    representation and that returning values works correctly.
    """
    t1 = Type("1")
    t2 = Type("2")
    type_chart = TypeChart({t1: {t2: 50}})
    assert 50 == type_chart.damage_modifier(t1, t2)
    assert 100 == type_chart.damage_modifier(Type("test"), t2)
    assert 100 == type_chart.damage_modifier(t1, Type("test"))
    assert "1 - (2:50), \n" == str(type_chart)


def test_type_chart_not_commutative():
    """
    The type chart should not be commutative by default: that is, if t1
    attacks t2 with efficacy of 200 that doesn't imply anything about
    t2 attacking t1.
    """
    t1 = Type("1")
    t2 = Type("2")
    type_chart = TypeChart({t1: {t2: 50}})
    assert 100 == type_chart.damage_modifier(t2, t1)
