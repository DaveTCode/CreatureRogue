"""
The creature object contains the information and immediately accessible
values for any creature.
"""

import math

from CreatureRogue.data_layer.species import Species
from CreatureRogue.data_layer.stat import Stat
from CreatureRogue.models.move import Move


class Creature:
    def __init__(
        self,
        species: Species,
        level: int,
        nickname: str | None,
        trainer,
        individual_values: dict[Stat, int],
        effort_values: dict[Stat, int],
        was_traded: bool,
        moves: list[Move],
        current_xp: int,
    ):
        self.species = species
        self.level = level
        self.nickname = nickname if nickname is not None else species.name
        self.trainer = trainer
        self.individual_values = individual_values
        self.effort_values = effort_values
        self.was_traded = was_traded
        self.moves = moves
        self.stats = {stat: self.max_stat(stat) for stat in species.base_stats}
        self.current_xp = current_xp
        self.fainted = False
        self.ailments = []

    def adjust_stat(self, stat: Stat, delta: int):
        """
        Adjust a stat by the given delta. Also caps at the min/max values
        for that stat.
        """
        self.stats[stat] -= delta

        if self.stats[stat] < 0:
            self.stats[stat] = 0
        elif self.stats[stat] > self.max_stat(stat):
            self.stats[stat] = self.max_stat(stat)

    def current_stat(self, stat: Stat) -> int:
        """
        Get the current value of the given stat.
        """
        return self.stats[stat]

    def max_stat(self, stat: Stat, level: int | None = None):
        """
        The stat value of a creature is a function of it's level, species,
        IVs and EVs and differs slightly for hitpoints and normal stats.

        Can optionally pass in a level to calculate what the stats were at
        a particular level.
        """
        if level is None:
            level = self.level

        if stat.name.upper() == "HP":
            value = (
                self.individual_values[stat]
                + self.species.base_stats[stat]
                + math.sqrt(self.effort_values[stat]) / 8
                + 50
            ) * level / 50 + 10
        else:
            value = (
                self.individual_values[stat]
                + self.species.base_stats[stat]
                + math.sqrt(self.effort_values[stat]) / 8
            ) * level / 50 + 5

        return int(value)

    def xp_given(self, number_winners, winner_traded, winner_modifier=1):
        """
        This corresponds to the number of experience points gained for
        defeating this creature.
        """
        xp_given = self.species.base_xp_yield * winner_modifier * self.level / (7 * number_winners)
        if winner_traded:
            xp_given *= 1.5
        if self.trainer is not None:
            xp_given *= 1.5

        return int(xp_given)

    def add_xp(self, xp_lookup, xp):
        """
        Increases the pokemon experience points. This can also cause a
        level up to occur.

        Returns messages indicating what has happened to be displayed by
        whatever calls this function.
        """
        self.current_xp += xp
        old_level = self.level
        self.level = self.species.level(xp_lookup, self.current_xp)

        messages = [f"{self.in_battle_name()} gains {xp} experience"]

        if old_level != self.level:
            messages.append(f"{self.in_battle_name()} is now level {self.level}!")

        return messages

    def in_battle_name(self):
        """
        When describing the creature in battle (e.g. to say "Wild pikachu
        fainted!") this is the name used.
        """
        if self.trainer:
            return f"{self.trainer.name}'s {self.nickname}"
        return f"Wild {self.nickname}"

    def __str__(self):
        return self.in_battle_name()
