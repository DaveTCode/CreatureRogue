'''
    The battle state is the main state that the game is in when the player is
    in a battle.

    It is responsible for rendering and input processing.
'''

import collections
import random
import CreatureRogue.data as data
import CreatureRogue.libtcodpy as libtcod

class BattleState():

    def __init__(self, game, game_data, renderer, level_up_renderer):
        self.renderer = renderer
        self.level_up_renderer = level_up_renderer
        self.game_data = game_data
        self.game = game
        self.messages = collections.deque()
        self.end_battle = False
        self.display_level_up = None

    def handle_input(self, key):
        '''
            Handle key input when in the battle state. Takes a single key at a 
            time but is only called when there is a key press.
        '''
        battle_data = self.game_data.battle_data

        if len(self.messages) > 0:
            if key.vk == libtcod.KEY_SPACE or key.vk == libtcod.KEY_ENTER:
                self.messages.popleft()
        elif self.display_level_up:
            if key.vk == libtcod.KEY_SPACE or key.vk == libtcod.KEY_ENTER:
                self.display_level_up = None
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
                    if random.randint(0, 1) == 0:
                        first_move = (move, battle_data.player_creature, battle_data.defending_creature())
                        second_move = (computer_move, battle_data.defending_creature(), battle_data.player_creature)
                    else:
                        first_move = (computer_move, battle_data.defending_creature(), battle_data.player_creature)
                        second_move = (move, battle_data.player_creature, battle_data.defending_creature())

                for move, aggressor, defender in [first_move, second_move]:
                    # The move can actually be None if there were no valid 
                    # moves to select from.
                    if move:
                        messages = move.act(aggressor, defender, self.game.static_game_data)
                        
                        for message in messages:
                            self.messages.append(message)

                        # Check the state of the creatures, we don't end the battle 
                        # immediately because we still want to process any 
                        # remaining messages.
                        #
                        # We do need to break out though so that the fainted 
                        # creature can't have it's turn.
                        if defender.creature.fainted:
                            self._creature_fainted(aggressor, defender)

                        if aggressor.creature.fainted or defender.creature.fainted:
                            self.end_battle = True
                            break

    def _creature_fainted(self, aggressor, defender):
        '''
            Called when a creature faints during battle. Used to add experience 
            to the winner and check for level ups.
        '''
        xp_given = defender.creature.xp_given(1, False)

        old_level = aggressor.creature.level
        messages = aggressor.creature.add_xp(self.game.static_game_data.xp_lookup, xp_given)

        for message in messages:
            self.messages.append(message)

        if old_level != aggressor.creature.level:
            self.display_level_up = (aggressor, old_level)

    def render(self):
        '''
            Render the current state of the battle. Called as many times as 
            required by the game loop.
        '''
        console = self.renderer.render(self.game_data.battle_data, self.messages)

        if len(self.messages) == 0 and self.display_level_up != None:
            sub_console = self.level_up_renderer.render(self.display_level_up[0].creature, self.display_level_up[1])

            libtcod.console_blit(sub_console, 0, 0, 0, 0, console, 0, 0)

        # The check to see whether to end the battle is done once in the 
        # render function so that we can guarantee that it will get called
        # within a 30fps time frame.
        if len(self.messages) == 0 and self.display_level_up == None and self.end_battle:
            self.game.end_wild_battle()

        return console