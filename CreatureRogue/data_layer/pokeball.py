class Pokeball():

    def __init__(self, pokeball_id, name, catch_rate, top_color, bottom_color, display_char):
        self.pokeball_id = pokeball_id
        self.name = name
        self.catch_rate = catch_rate
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.display_char = display_char

    def __str__(self):
        return "{0}. {1}".format(self.display_char, self.name)