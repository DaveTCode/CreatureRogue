from CreatureRogue.data_layer.pokeball import Pokeball


def _create_default_pokeball() -> Pokeball:
    """
    A simple routine to create a default pokeball for use whilst testing.
    """
    return Pokeball(
        pokeball_id=1,
        name="test",
        catch_rate=2.0,
        top_color=(255, 0, 0),
        bottom_color=(255, 255, 255),
        display_char="p",
    )


def test_str_representation():
    """
    Check that the string representation of a pokeball makes sense.
    """
    p = _create_default_pokeball()
    assert str(p) == "p. test"
