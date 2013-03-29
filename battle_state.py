import collections
import data
import libtcodpy as libtcod
import random

class BattleState():

    def __init__(self, game, game_data, renderer):
        self.renderer = renderer
        self.game_data = game_data
        self.game = game
        self.messages = collections.deque()

    def handle_input(self, key):
        '''
            Handle key input when in the battle state. Takes a single key at a 
            time but is only called when there is a key press.
        '''
        battle_data = self.game_data.battle_data

        if len(self.messages) > 0:
            if key.vk == libtcod.KEY_SPACE or key.vk == libtcod.KEY_ENTER:
                self.messages.popleft()
        else:
            move = None
            for key_code, index in [(libtcod.KEY_1, 0), (libtcod.KEY_2, 1), (libtcod.KEY_3, 2), (libtcod.KEY_4, 3)]:
                if key.vk == key_code:
                    if len(battle_data.player_creature.creature.moves) > index:
                        move = battle_data.player_creature.creature.moves[index]

            if move != None:
                computer_move = battle_data.computer_move()
                speed_stat = self.game.static_game_data.stats[data.SPEED_STAT]

                if battle_data.player_creature.stat_value(speed_stat) > battle_data.defending_creature().stat_value(speed_stat):
                    first_move = (move, battle_data.player_creature, battle_data.defending_creature())
                    second_move = (computer_move, battle_data.defending_creature(), battle_data.player_creature)
                elif battle_data.player_creature.stat_value(speed_stat) < battle_data.defending_creature().stat_value(speed_stat):
                    first_move = (computer_move, battle_data.defending_creature(), battle_data.player_creature)
                    second_move = (move, battle_data.player_creature, battle_data.defending_creature())
                else:
                    r = random.randint(0, 1)
                    if r == 0:
                        first_move = (move, battle_data.player_creature, battle_data.defending_creature())
                        second_move = (computer_move, battle_data.defending_creature(), battle_data.player_creature)
                    else:
                        first_move = (computer_move, battle_data.defending_creature(), battle_data.player_creature)
                        second_move = (move, battle_data.player_creature, battle_data.defending_creature())

                for move, aggressor, defender in [first_move, second_move]:
                    messages = move.act(aggressor, defender, self.game.static_game_data)
                    
                    for message in messages:
                        self.messages.append(message)

                    # TODO - Check battle state now.

    def render(self):
        '''
            Render the current state of the battle. Called as many times as 
            required by the game loop.
        '''
        self.renderer.render(self.game_data.battle_data, self.messages)