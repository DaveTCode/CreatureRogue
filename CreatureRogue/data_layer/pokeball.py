class Pokeball:
    def __init__(
        self,
        pokeball_id: int,
        name: str,
        catch_rate: float,
        top_color: tuple[int, int, int],
        bottom_color: tuple[int, int, int],
        display_char: str,
    ):
        self.pokeball_id = pokeball_id
        self.name = name
        self.catch_rate = catch_rate
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.display_char = display_char

    def __str__(self):
        return f"{self.display_char}. {self.name}"
