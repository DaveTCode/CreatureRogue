class MoveData:

    def __init__(self, name, max_pp, type, base_attack, base_accuracy, min_hits, max_hits, stat_changes, attack_stat, defence_stat, accuracy_stat, evasion_stat, target, ailment):
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

    def damage_move(self):
        """
            Determines whether a move affects the targets health.
        """
        return self.attack_stat is not None

    def stat_change_move(self):
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
