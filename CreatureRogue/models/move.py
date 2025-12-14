from CreatureRogue.data_layer.move_data import MoveData


class Move:
    """
    A move is a single action that a creature can take during a battle.
    """

    def __init__(self, move_data: MoveData):
        self.move_data = move_data
        self.pp = self.move_data.max_pp
