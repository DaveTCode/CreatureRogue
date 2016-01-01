class Species:
    def __init__(self, pokedex_number, name, height, weight, types, base_stats, base_xp_yield, growth_rate, display_character, display_color, level_moves, flavor_text, genus, capture_rate):
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

    def imperial_weight_str(self):
        """
            Weight is stored in 1/10kg so this function is used to convert to
            an appropriate imperial viewing string of lbs.
        """
        return '{0:.1f} lbs.'.format(self.weight / 10 * 2.20462)

    def imperial_height_str(self):
        """
            Height is stored in 1/10m in the database so this function is used
            to convert into an imperial display format of feet and inches.
        """
        feet = self.height / 10 * 3.2808399
        inches = (feet % 1) * 12

        return '{0}\'{1:0=2d}"'.format(int(feet), int(round(inches)))

    def move_data_at_level(self, level):
        """
            When a wild creature is encountered, it's move set is the most
            recent 4 moves that it would have learnt from leveling up.

            This function calculates that set of moves (may be less than 4).
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