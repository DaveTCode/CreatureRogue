from CreatureRogue.data_layer.ailment import Ailment


def test_string_blank_name():
    a = Ailment(0, "")
    assert str(a) == ""


def test_string_real_name():
    a = Ailment(0, "Hello I'm a name")
    assert str(a) == "Hello I'm a name"
