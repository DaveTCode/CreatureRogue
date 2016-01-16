"""
    A move is a single action that a creature can take during a battle.
"""


class Move:
    def __init__(self, move_data):
        self.move_data = move_data
        self.pp = self.move_data.max_pp
