from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class GameData:
    """
    The game data is the main object that is handled by the game.

    It contains all game state and information on top level objects.
    """

    def __init__(self):
        self.is_in_battle = True
        self.battle_data = None  # type: BattleData | None
        self.player = None  # type: Player | None
