'''
    The game data is the main object that is handled by the game.

    It contains all game state and information on top level objects.
'''
class GameData():
        
    def __init__(self):
        self.is_in_battle = True
        self.battle_data = None
        self.player = None