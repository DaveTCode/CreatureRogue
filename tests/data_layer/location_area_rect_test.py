from CreatureRogue.data_layer.location_area_rect import LocationAreaRect


def test_str_representation():
    location_area = LocationAreaRect(location_area_id=1, x1=100, x2=120, y1=200, y2=220)
    assert str(location_area) == "1 - (100,200),(120,220)"
