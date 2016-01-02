from typing import Optional, Mapping

from CreatureRogue.data_layer.ailment import Ailment
from CreatureRogue.data_layer.move_target import MoveTarget
from CreatureRogue.data_layer.stat import Stat
from CreatureRogue.data_layer.type import Type


class MoveData:

    def __init__(self, name: str, max_pp: int, type: Type, base_attack: int, base_accuracy: int,
                 min_hits: int, max_hits: int, stat_changes: Mapping[Stat, int],
                 attack_stat: Optional[Stat], defence_stat: Optional[Stat], accuracy_stat: Optional[Stat], evasion_stat: Optional[Stat],
                 target: MoveTarget, ailment: Optional[Ailment]):
        self.name = name
        self.max_pp = max_pp
        self.type = type
        self.base_attack = base_attack
        self.base_accuracy = base_accuracy
        self.attack_stat = attack_stat
        self.defence_stat = defence_stat
        self.accuracy_stat = accuracy_stat
        self.evasion_stat = evasion_stat
        self.min_hits = min_hits
        self.max_hits = max_hits
        self.stat_changes = stat_changes
        self.target = target
        self.ailment = ailment

    def damage_move(self) -> bool:
        """
            Determines whether a move affects the targets health.
        """
        return self.attack_stat is not None

    def stat_change_move(self) -> bool:
        """
            Determines whether a move affects the targets stats. This is
            independent of whether it affects their health.
        """
        for stat in self.stat_changes:
            if self.stat_changes[stat] != 0:
                return True

        return False

    def __str__(self):
        return self.name
