"""
    AIs used to determine which move to pick in a battle.
"""
from random import choice


class RandomMoveAi:
    """
        AI which just selects any move at random from the pool of available
        ones (i.e. those with PP > 0).
    """

    def __init__(self, battle_creature):
        self.battle_creature = battle_creature

    def select_move(self):
        """
            Should use struggle if the creature has no moves. Just doesn't 
            select a move for now.
        """
        pp_moves = [move for move in self.battle_creature.creature.moves if move.pp > 0]
        if len(pp_moves) == 0:
            return None

        return choice(pp_moves)