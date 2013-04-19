'''
    A map object contains information on what tiles to display but does 
    not hold the information on where the player is.
'''
class Map():
    
    def __init__(self, name, tiles):
        self.name = name
        self.tiles = tiles