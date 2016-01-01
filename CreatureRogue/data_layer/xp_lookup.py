class XpLookup:
    def __init__(self, xp_map):
        self.xp_map = xp_map

    def level_at_xp(self, species, xp):
        """
            The level that a creature is when it has exactly xp amount of
            experience is determined by the species growth rate and some static
            data which is checked here.
        """
        level_xps = self.xp_map[species.growth_rate]

        for level, level_xp in level_xps.iteritems():
            if xp < level_xp:
                return level

        return 0

    def xp_at_level(self, species, level):
        """
            This is the minimum XP required to achieve a certain level for the
            given species.
        """
        return self.xp_map[species.growth_rate][level]