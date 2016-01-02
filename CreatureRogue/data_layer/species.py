from typing import Sequence, Mapping

from CreatureRogue.data_layer.color import Color
from CreatureRogue.data_layer.growth_rate import GrowthRate
from CreatureRogue.data_layer.move_data import MoveData
from CreatureRogue.data_layer.type import Type
from CreatureRogue.data_layer.stat import Stat


class Species:
    def __init__(self, pokedex_number: int, name: str, height: int, weight: int,
                 types: Sequence[Type], base_stats: Sequence[Stat], base_xp_yield: int,
                 growth_rate: GrowthRate, display_character: str, display_color: Color,
                 level_moves: Mapping[int, MoveData], flavor_text: str, genus: str, capture_rate: int):
        self.pokedex_number = pokedex_number
        self.name = name
        self.height = height
        self.weight = weight
        self.types = types
        self.base_stats = base_stats
        self.base_xp_yield = base_xp_yield
        self.growth_rate = growth_rate
        self.display_character = display_character
        self.display_color = display_color
        self.level_moves = level_moves
        self.flavor_text = flavor_text
        self.genus = genus
        self.capture_rate = capture_rate

    def imperial_weight_str(self) -> str:
        """
            Weight is stored in 1/10kg so this function is used to convert to
            an appropriate imperial viewing string of lbs.
        """
        return '{0:.1f} lbs.'.format(self.weight / 10 * 2.20462)

    def imperial_height_str(self) -> str:
        """
            Height is stored in 1/10m in the database so this function is used
            to convert into an imperial display format of feet and inches.
        """
        feet = self.height / 10 * 3.2808399
        inches = (feet % 1) * 12

        return '{0}\'{1:0=2d}"'.format(int(feet), int(round(inches)))

    def move_data_at_level(self, level: int) -> Sequence[MoveData]:
        """
            When a wild creature is encountered, it's move set is the most
            recent 4 moves that it would have learnt from leveling up.

            This function calculates that set of moves (may be less than 4).

            :param level: The level at which we want a list of moves.

            :returns: A list of the first 4 moves that the species would have
            learnt by the level passed in.
        """
        moves = []
        for i in range(level, 0, -1):
            moves = moves + self.level_moves[i]

            if len(moves) >= 4:
                break

        return moves[:4]

    def level(self, xp_loader, current_xp):
        """
            The level of a species is determined solely by its current xp.
        """
        return xp_loader.level_at_xp(self, current_xp)

    def __str__(self):
        return self.name
