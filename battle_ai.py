from random import choice

class RandomMoveAi():
    '''
        AI which just selects any move at random from the pool of available
        ones (i.e. those with PP > 0).
    '''

    def __init__(self, battle_creature):
        self.battle_creature = battle_creature

    def select_move(self, moves):
        '''
            Will break if no move has PP > 0. Need to fix at some point.
        '''
        return choice(filter(lambda move: move.pp > 0, self.battle_creature.creature.moves))