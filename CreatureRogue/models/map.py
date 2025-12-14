class Map:
    """
    A map object contains information on what tiles to display but does
    not hold the information on where the player is.
    """

    def __init__(self, name: str, tiles):
        self.name = name
        self.tiles = tiles
