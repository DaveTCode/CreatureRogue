from __future__ import division
import math
import random
import sys
import collections

class BattleCreature():
    def __init__(self, creature, static_game_data):
        self.creature = creature
        self.stats = {stat: self.creature.species.base_stats[stat] for stat in self.creature.species.base_stats}
        self.stats[static_game_data.accuracy_stat()] = 1
        self.stats[static_game_data.evasion_stat()] = 1

class Creature():
    
    def __init__(self, species, level, nickname, trainer, individual_values, effort_values, was_traded, moves, current_xp):
        self.species = species
        self.level = level
        self.nickname = nickname if nickname != None else species.name
        self.trainer = trainer
        self.individual_values = individual_values
        self.effort_values = effort_values
        self.was_traded = was_traded
        self.moves = moves
        self.stats = {stat: self.max_stat(stat) for stat in species.base_stats}
        self.current_xp = current_xp
        
    def adjust_stat(self, stat, delta):
        self.stats[stat] = self.stats[stat] - delta
        
        if self.stats[stat] < 0:
            self.stats[stat] = 0
        elif self.stats[stat] > self.max_stat(stat):
            self.stats[stat] = self.max_stat(stat)
        
    def current_stat(self, stat):
        return self.stats[stat]
        
    def max_stat(self, stat):
        '''
            The stat value of a creature is a function of it's level, species,
            IVs and EVs and differs slightly for hitpoints and normal stats.
        '''
        if stat.name.upper() == "HP":
            value = (self.individual_values[stat] + self.species.base_stats[stat] + math.sqrt(self.effort_values[stat]) / 8 + 50) * self.level / 50 + 10
        else:
            value = (self.individual_values[stat] + self.species.base_stats[stat] + math.sqrt(self.effort_values[stat]) / 8) * self.level / 50 + 5
            
        return int(value)
        
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
        
        return int(xp)
        
class Player():

    def __init__(self, name, static_game_data):
        self.name = name
        self.creatures = []
        self.pokedex = { static_game_data.species[id].pokedex_number: (0, static_game_data.species[id]) for id in static_game_data.species }
        
class GameData():
        
    def __init__(self):
        self.is_in_battle = True
        self.battle_data = BattleData(self, None, None, None)
        
class BattleData():

    def __init__(self, game_data, player_creature, trainer_creature=None, wild_creature=None):
        self.game_data = game_data
        self.player_creature = player_creature
        self.wild_creature = wild_creature
        self.trainer_creature = trainer_creature
        self.messages_to_display = collections.deque()

    def defending_creature(self):
        return self.trainer_creature if self.trainer_creature != None else self.wild_creature
        
    def pop_message(self):
        if (len(self.messages_to_display) > 0):
            return self.messages_to_display.popleft()
        else:
            return None
            
class Move():
    def __init__(self, move_data):
        self.move_data = move_data
        self.pp = self.move_data.max_pp
        
    def act(self, attacking_creature, defending_creature, static_game_data):
        messages = []
    
        if self.pp <= 0:
            messages.append('Not enough points to perform ' + self.move_data.name)
        else:
            messages.append(attacking_creature.creature.nickname + ' used ' + self.move_data.name)
            self.pp = self.pp - 1
        
            # Check if the move misses
            if not self._hit_calculation(attacking_creature, defending_creature):
                messages.append(attacking_creature.creature.nickname + "'s attack missed!")
            else:
                if self.move_data.damage_move():
                    new_messages, hp_loss = self._damage_calculation(attacking_creature, defending_creature, static_game_data.type_chart)
                    
                    for message in new_messages:
                        messages.append(message)
                        
                    defending_creature.creature.adjust_stat(static_game_data.hp_stat(), hp_loss)
                    
                    # TODO: Handle stat changes. Needs concept of move target
                    
        return messages
                
    def _hit_calculation(self, attacking_creature, defending_creature):
        p = self.move_data.base_accuracy / 100 * (attacking_creature.stats[self.move_data.accuracy_stat] / defending_creature.stats[self.move_data.evasion_stat])
        r = random.random()
        
        return r < p
    
    def _damage_calculation(self, attacking_creature, defending_creature, type_chart):
        '''
            To calculate the damage that a move does we need to know which
            creature is performing the move and which is defending it.
            
            The return value for this is the hitpoint delta.
        '''
        attack_stat_value = attacking_creature.stats[self.move_data.attack_stat]
        defence_stat_value = defending_creature.stats[self.move_data.defence_stat]
        
        # Modifiers
        critical_modifier = 2 if random.uniform(0, 100) < 6.25 else 1 # TODO: Incomplete - should use items and check whether this is a high critical move etc
        same_type_attack_bonus = 1.5 if self.move_data.type in attacking_creature.creature.species.types else 1
        type_modifier = 1
        for type in defending_creature.creature.species.types:
            type_modifier = type_modifier * type_chart.damage_modifier(self.move_data.type, type) / 100
            
        modifier = same_type_attack_bonus * type_modifier * critical_modifier # TODO: Incomplete - Ignoring weather effects and other bits
        
        messages = []
        if critical_modifier > 1:
            messages.append('Critical hit!')
        if type_modifier == 0:
            messages.append('The attack had no effect!')
        elif type_modifier < 0.9:
            messages.append('The attack was not very effective')
        elif type_modifier > 1.1:
            messages.append('The attack was super effective!')
            
        return messages, int((((2 * attacking_creature.creature.level + 10) / 250) * (attack_stat_value / defence_stat_value) * self.move_data.base_attack + 2) * modifier)