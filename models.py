from __future__ import division
from maps.map_renderer import *
from map_loader import MapLoader
import math
import random
import sys
import collections

class BattleCreature():
    stat_adjust_factors = {-6: 1/4, -5: 2/7, -4: 1/3, -3: 2/5, -2: 1/2, -1: 2/3, 
                           0: 1.0, 
                           1: 1.5, 2: 2.0, 3: 2.5, 4: 3.0, 5: 3.5, 6: 4.0}

    def __init__(self, creature, static_game_data):
        self.creature = creature
        self.stats = {stat: self.creature.species.base_stats[stat] for stat in self.creature.species.base_stats}
        self.stats[static_game_data.accuracy_stat()] = 1
        self.stats[static_game_data.evasion_stat()] = 1
        self.stat_adjusts = {stat: 0 for stat in self.creature.species.base_stats}
        self.stat_adjusts[static_game_data.accuracy_stat()] = 0
        self.stat_adjusts[static_game_data.evasion_stat()] = 0
        
    def adjust_stat_adjusts(self, stat, value):
        '''
            The only adjustment to statistics of a creature in battle is done 
            through these factors which range from -6 to 6.
            
            Returns the amount by which we actually adjusted the stat.
        '''
        old_val = self.stat_adjusts[stat]
        self.stat_adjusts[stat] += value
        
        if self.stat_adjusts[stat] > 6:
            self.stat_adjusts[stat] = 6
        elif self.stat_adjusts[stat] < -6:
            self.stat_adjusts[stat] = -6
            
        return self.stat_adjusts[stat] - old_val
        
    def stat_value(self, stat):
        '''
            The current value of a stat in battle is the base stat for that 
            creature (i.e. the value pre battle) multiplied by the factor
            gained from moves performed on the creature during battle.
            
            These factors are fixed and are capped at 1/4 to 4.
        '''
        return self.stats[stat] * BattleCreature.stat_adjust_factors[self.stat_adjusts[stat]]

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

    def __init__(self, name, static_game_data, location_area, x, y):
        self.name = name
        self.creatures = []
        self.pokedex = { static_game_data.species[id].pokedex_number: (0, static_game_data.species[id]) for id in static_game_data.species }
        self.location_area = location_area
        self.coords = (x, y)
        self.steps_in_long_grass_since_encounter = 0
        self.static_game_data = static_game_data
        
    def _can_traverse(self, cell):
        # TODO - Only really check that the cell is always travesable at the moment
        return cell.base_cell.cell_passable_type == EMPTY_CELL

    def _causes_encounter(self):
        encounter_rate = 100 if self.location_area.rate > 100 else self.location_area.rate

        if 8 - encounter_rate // 10 < self.steps_in_long_grass_since_encounter:
            if random.random() < 0.95:
                return False

        if random.randint(0, 99) < encounter_rate and random.randint(0, 99) < 40:
            return True
        else:
            return False

    def move_to_cell(self, x, y):
        '''
            Move to the cell specified by x,y in the current map.

            Returns (whether moved, whether caused a wild encounter)
        '''
        if self._can_traverse(self.location_area.map.tiles[y][x]):
            self.coords = (x, y)
            causes_encounter = False

            if (self.location_area.map.tiles[y][x].exit_location != None):
                self.location_area = self.static_game_data.location_areas[self.location_area.map.tiles[y][x].exit_location]
                self.steps_in_long_grass_since_encounter = 0
            else:
                if self.get_cell().base_cell == LONG_GRASS:
                    self.steps_in_long_grass_since_encounter += 1

                    causes_encounter = self._causes_encounter()
                else:
                    self.steps_in_long_grass_since_encounter = 0

            return True, causes_encounter
        else:
            return false, None

    def get_cell(self):
        return self.map.tiles[self.coords[1], self.coords[0]]
        
class GameData():
        
    def __init__(self):
        self.is_in_battle = True
        self.battle_data = None
        
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
                            
                        target.creature.adjust_stat(static_game_data.hp_stat(), hp_loss)
                        
                    if self.move_data.stat_change_move():
                        for stat in self.move_data.stat_changes:
                            # Returns the amount by which the stat was adjusted
                            adjust_amount = target.adjust_stat_adjusts(stat, self.move_data.stat_changes[stat])
                            if adjust_amount == 0 and self.move_data.stat_changes[stat] != 0 and not self.move_data.damage_move():
                                direction = 'higher' if self.move_data.stat_changes[stat] > 0 else 'lower'
                                messages.append('{0}\'s {1} won\'t go any {2}!'.format(target.creature.nickname, stat.name, direction))
                            elif adjust_amount == 1:
                                messages.append('{0}\'s {1} rose!'.format(target.creature.nickname, stat.name))
                            elif adjust_amount == 2:
                                messages.append('{0}\'s {1} sharply rose!'.format(target.creature.nickname, stat.name))
                            elif adjust_amount > 2:
                                messages.append('{0}\'s {1} rose drastically!'.format(target.creature.nickname, stat.name))
                            elif adjust_amount == -1:
                                messages.append('{0}\'s {1} fell!'.format(target.creature.nickname, stat.name))
                            elif adjust_amount == -2:
                                messages.append('{0}\'s {1} harshly fell!'.format(target.creature.nickname, stat.name))
                            elif adjust_amount < -2:
                                messages.append('{0}\'s {1} severely fell!'.format(target.creature.nickname, stat.name))
                    
        return messages
                
    def _hit_calculation(self, attacking_creature, defending_creature):
        p = self.move_data.base_accuracy / 100 * (attacking_creature.stat_value(self.move_data.accuracy_stat) / defending_creature.stat_value(self.move_data.evasion_stat))
        r = random.random()
        
        return r < p
    
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
        
class Map():
    
    def __init__(self, location_area, tiles):
        self.tiles = tiles
        self.location_area = location_area