class MapDataTileType:
    def __init__(
        self, name: str, display_character: str, red: int, green: int, blue: int, traversable: bool
    ):
        self.name = name
        self.display_character = display_character
        self.red = red
        self.green = green
        self.blue = blue
        self.traversable = (
            traversable  # TODO - What sort of traversable? Not coded into anything yet.
        )

    @property
    def color(self) -> tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    def __str__(self):
        return self.name
