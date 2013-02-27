class Creature():
    
    def __init__(self, species, level, nickname, trainer, individual_values, effort_values, was_traded, moves, stats):
        self.species = species
        self.level = level
        self.nickname = nickname
        self.trainer = trainer
        self.individual_values = individual_values
        self.effort_values = effort_values
        self.was_traded = was_traded
        self.moves = [{'move': move, 'pp': move.max_pp} for move in moves]
        self.stats = stats
        
        self.current_hp = self.max_hp()
        
    def max_hp(self):
        '''
            The maximum hit points of a creature is a function of it's level,
            species, IVs and EVs
        '''
        return math.floor((self.species.base_hp + self.individual_values["hp"] + math.sqrt(self.effort_values["hp"]) / 8 + 50) * self.level / 50 + 10)
        
    def xp_given(self, number_winners, winner_traded, winner_modifier = 1):
        '''
            This corresponds to the number of experience points gained for 
            defeating this creature.
        '''
        xp = self.species.base_xp_yield * winner_modifier * self.level / (7 * number_winners)
        if self.trainer != None:
            xp = xp * 1.5
        if winner_traded:
            xp = xp * 1.5
        
        return math.floor(xp)