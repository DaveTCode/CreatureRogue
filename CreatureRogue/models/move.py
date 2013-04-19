'''
    A move is a single action that a creature can take during a battle.
'''
from __future__ import division
import random
from CreatureRogue.data import data

class Move():
    def __init__(self, move_data):
        self.move_data = move_data
        self.pp = self.move_data.max_pp
        
    def act(self, attacking_creature, defending_creature, static_game_data):
        '''
            Perform the move on the defending creature. 

            Will return a list of messages indicating what has happened.
        '''
        messages = []
    
        if self.pp <= 0:
            messages.append(u"Not enough points to perform {0}".format(self.move_data.name))
        else:
            messages.append(u"{0} used {1}".format(attacking_creature.creature.in_battle_name(), self.move_data.name))
            self.pp -= 1
        
            # Check if the move misses
            if not self._hit_calculation(attacking_creature, defending_creature):
                messages.append(u"{0}'s attack missed!".format(attacking_creature.creature.in_battle_name()))
            else:
                # TODO: Missing the "specific-move" target and only considering 1v1 battles.
                target = None
                if self.move_data.target.identifier in ['user', 'users-field', 'user-or-ally', 'entire-field']:
                    target = attacking_creature
                if self.move_data.target.identifier in ['selected-pokemon', 'random-opponent', 'all-other-pokemon', 'opponents-field', 'all-opponents', 'entire-field']:
                    target = defending_creature
            
                if target:
                    if self.move_data.damage_move():
                        new_messages, hp_loss = self._damage_calculation(attacking_creature, target, static_game_data.type_chart)
                        
                        for message in new_messages:
                            messages.append(message)
                            
                        hp_stat = static_game_data.stat(data.HP_STAT)
                        target.creature.adjust_stat(hp_stat, hp_loss)

                        if target.stat_value(hp_stat) <= 0:
                            target.creature.fainted = True
                            messages.append(u"{0} fainted!".format(target.creature.in_battle_name()))
                        
                    if self.move_data.stat_change_move():
                        for stat in self.move_data.stat_changes:
                            adjust_amount = target.adjust_stat_adjusts(stat, self.move_data.stat_changes[stat])

                            if adjust_amount == 0 and self.move_data.stat_changes[stat] != 0 and not self.move_data.damage_move():
                                direction = 'higher' if self.move_data.stat_changes[stat] > 0 else 'lower'
                                messages.append(u"{0}'s {1} won't go any {2}!".format(target.creature.in_battle_name(), stat.name, direction))
                            elif adjust_amount == 1:
                                messages.append(u"{0}'s {1} rose!".format(target.creature.in_battle_name(), stat.name))
                            elif adjust_amount == 2:
                                messages.append(u"{0}'s {1} sharply rose!".format(target.creature.in_battle_name(), stat.name))
                            elif adjust_amount > 2:
                                messages.append(u"{0}'s {1} rose drastically!".format(target.creature.in_battle_name(), stat.name))
                            elif adjust_amount == -1:
                                messages.append(u"{0}'s {1} fell!".format(target.creature.in_battle_name(), stat.name))
                            elif adjust_amount == -2:
                                messages.append(u"{0}'s {1} harshly fell!".format(target.creature.in_battle_name(), stat.name))
                            elif adjust_amount < -2:
                                messages.append(u"{0}'s {1} severely fell!".format(target.creature.in_battle_name(), stat.name))
                    
        return messages
                
    def _hit_calculation(self, attacking_creature, defending_creature):
        '''
            Determines whether the current move will hit the defending 
            creature. This is based on a random check.
        '''
        if self.move_data.base_accuracy:
            return random.random() < (self.move_data.base_accuracy / 100 * 
                                      (attacking_creature.stat_value(self.move_data.accuracy_stat) / 
                                       defending_creature.stat_value(self.move_data.evasion_stat)))
        
        return False
    
    def _damage_calculation(self, attacking_creature, defending_creature, type_chart):
        '''
            To calculate the damage that a move does we need to know which
            creature is performing the move and which is defending it.
            
            The return value for this is the hitpoint delta.
        '''
        attack_stat_value = attacking_creature.stat_value(self.move_data.attack_stat)
        defence_stat_value = defending_creature.stat_value(self.move_data.defence_stat)
        
        # Modifiers
        critical_modifier = 2 if random.uniform(0, 100) < 6.25 else 1 # TODO: Incomplete - should use items and check whether this is a high critical move etc
        same_type_attack_bonus = 1.5 if self.move_data.type in attacking_creature.creature.species.types else 1
        type_modifier = 1
        for defending_type in defending_creature.creature.species.types:
            type_modifier = type_modifier * type_chart.damage_modifier(self.move_data.type, defending_type) / 100
            
        modifier = same_type_attack_bonus * type_modifier * critical_modifier # TODO: Incomplete - Ignoring weather effects and other bits
        
        messages = []
        if critical_modifier > 1:
            messages.append("Critical hit!")
        if type_modifier == 0:
            messages.append("The attack had no effect!")
        elif type_modifier < 0.9:
            messages.append("The attack was not very effective")
        elif type_modifier > 1.1:
            messages.append("The attack was super effective!")
            
        return messages, int((((2 * attacking_creature.creature.level + 10) / 250) * (attack_stat_value / defence_stat_value) * self.move_data.base_attack + 2) * modifier)