from CreatureRogue.data_layer.color import Color


class Pokeball:
    def __init__(self, pokeball_id: int, name: str, catch_rate: float, top_color: Color, bottom_color: Color, display_char: str):
        self.pokeball_id = pokeball_id
        self.name = name
        self.catch_rate = catch_rate
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.display_char = display_char

    def __str__(self):
        return "{0}. {1}".format(self.display_char, self.name)
