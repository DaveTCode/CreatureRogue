"""
    This information is the core data used when the main game state is 
    "in battle".

    It contains information on the participants.
"""


class BattleData:
    def __init__(self, game_data, player_creature, computer_ai, trainer_creature=None, wild_creature=None):
        self.game_data = game_data
        self.player_creature = player_creature
        self.wild_creature = wild_creature
        self.trainer_creature = trainer_creature
        self.computer_ai = computer_ai

    def defending_creature(self):
        """
            The defending creature can either be wild or a trainer creature.

            This abstraction allows us to guarantee we always get the right 
            one.
        """
        return self.trainer_creature if self.trainer_creature is not None else self.wild_creature

    def computer_move(self):
        """
            Selects a move based on whatever computer ai is in use.
        """
        return self.computer_ai.select_move()
