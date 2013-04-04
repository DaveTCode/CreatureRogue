from __future__ import division
import math
import random

import CreatureRogue.maps.map_renderer as map_renderer
import CreatureRogue.data as data

class BattleCreature():
    stat_adjust_factors = {-6: 1/4, -5: 2/7, -4: 1/3, -3: 2/5, -2: 1/2, -1: 2/3, 
                           0: 1.0, 
                           1: 1.5, 2: 2.0, 3: 2.5, 4: 3.0, 5: 3.5, 6: 4.0}

    def __init__(self, creature, static_game_data):
        self.creature = creature
        self.stat_adjusts = {stat: 0 for stat in self.creature.stats}
        
    def adjust_stat_adjusts(self, stat, value):
        '''
            The only adjustment to statistics of a creature in battle is done 
            through these factors which range from -6 to 6.
            
            Returns the amount by which we actually adjusted the stat.
        '''
        old_val = self.stat_adjusts[stat]
        self.stat_adjusts[stat] += value
        
        self.stat_adjusts[stat] = max(-6, min(6, self.stat_adjusts[stat]))
            
        return self.stat_adjusts[stat] - old_val
        
    def stat_value(self, stat):
        '''
            The current value of a stat in battle is the base stat for that 
            creature (i.e. the value pre battle) multiplied by the factor
            gained from moves performed on the creature during battle.
            
            These factors are fixed and are capped at 1/4 to 4.
        '''
        return self.creature.stats[stat] * BattleCreature.stat_adjust_factors[self.stat_adjusts[stat]]

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
        self.fainted = False
        
    def adjust_stat(self, stat, delta):
        self.stats[stat] = self.stats[stat] - delta
        
        if self.stats[stat] < 0:
            self.stats[stat] = 0
        elif self.stats[stat] > self.max_stat(stat):
            self.stats[stat] = self.max_stat(stat)
        
    def current_stat(self, stat):
        return self.stats[stat]
        
    def max_stat(self, stat, level=None):
        '''
            The stat value of a creature is a function of it's level, species,
            IVs and EVs and differs slightly for hitpoints and normal stats.

            Can optionally pass in a level to calculate what the stats were at
            a particular level.
        '''
        if level == None:
            level = self.level

        if stat.name.upper() == "HP":
            value = (self.individual_values[stat] + self.species.base_stats[stat] + math.sqrt(self.effort_values[stat]) / 8 + 50) * level / 50 + 10
        else:
            value = (self.individual_values[stat] + self.species.base_stats[stat] + math.sqrt(self.effort_values[stat]) / 8) * level / 50 + 5
            
        return int(value)
        
    def xp_given(self, number_winners, winner_traded, winner_modifier = 1):
        '''
            This corresponds to the number of experience points gained for 
            defeating this creature.
        '''
        xp_given = self.species.base_xp_yield * winner_modifier * self.level / (7 * number_winners)
        if winner_traded:
            xp_given *= 1.5
        if self.trainer != None:
            xp_given *= 1.5
        
        return int(xp_given)

    def add_xp(self, xp_lookup, xp):
        '''
            Increases the pokemon experience points. This can also cause a 
            level up to occur.

            Returns messages indicating what has happened to be displayed by
            whatever calls this function.
        '''
        self.current_xp += xp
        old_level = self.level
        self.level = self.species.level(xp_lookup, self.current_xp)

        messages = [u"{0} gains {1} experience".format(self.in_battle_name(), xp)]

        if old_level != self.level:
            messages.append(u"{0} is now level {1}!".format(self.in_battle_name(), self.level))

        return messages

    def in_battle_name(self):
        '''
            When describing the creature in battle (e.g. to say "Wild pikachu 
            fainted!") this is the name used.
        '''
        if self.trainer:
            return u"{0}'s {1}".format(self.trainer.name, self.nickname)
        else:
            return u"Wild {0}".format(self.nickname)
        
class Player():

    def __init__(self, name, static_game_data, map_data, x, y):
        self.name = name
        self.creatures = []
        self.pokedex = { static_game_data.species[species_id].pokedex_number: (0, static_game_data.species[species_id]) for species_id in static_game_data.species }
        self.map_data = map_data
        self.coords = (x, y)
        self.steps_in_long_grass_since_encounter = 0
        self.static_game_data = static_game_data
        self.pokeballs = { static_game_data.pokeballs[pokeball_id]: 0 for pokeball_id in static_game_data.pokeballs }
        
    def available_pokeballs(self):
        '''
            Checks whether the player has any available pokeballs.
        '''
        return { pokeball: self.pokeballs[pokeball] for pokeball in self.pokeballs if self.pokeballs[pokeball] > 0 }

    def get_location_area(self):
        '''
            The location area of a player is determined by the x, y coordinates 
            and the static game data.
        '''
        x, y = self.coords
        location_area_id = self.static_game_data.location_area_rects.get_location_area_by_position(x, y)

        print location_area_id
        if location_area_id != None:
            location_area = self.static_game_data.location_areas[location_area_id]

            return location_area

        return None

    def _can_traverse(self, cell):
        '''
            Depending on the current player state they may or may not be able 
            to traverse any given cell. This check is made every time the 
            player attempts to move onto a new cell.

            Returns true if the player is allowed to travel on that cell and
            false otherwise.
        '''
        # TODO - Only really check that the cell is always travesable at the moment
        return cell.base_cell.cell_passable_type == map_renderer.EMPTY_CELL

    def _causes_encounter(self):
        '''
            Calculation used to determine whether a player causes an encounter 
            with movement.

            It is called each time the player steps on a square that could 
            cause an encounter and returns true if an encounter should be 
            generated and false otherwise.
        '''
        location_area = self.get_location_area()
        encounter_rate = min(100, location_area.walk_encounter_rate)

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
        if self._can_traverse(self.map_data.tiles[y][x]):
            self.coords = (x, y)
            causes_encounter = False

            if self.get_cell().base_cell == map_renderer.LONG_GRASS:
                self.steps_in_long_grass_since_encounter += 1

                causes_encounter = self._causes_encounter()
            else:
                self.steps_in_long_grass_since_encounter = 0

            return True, causes_encounter
        else:
            return False, False

    def get_cell(self):
        '''
            Returns the exact cell that the player is currently on.
        '''
        return self.map_data.tiles[self.coords[1]][self.coords[0]]

    def encounter_creature(self, creature):
        '''
            Called whenever a creature is encountered (even it it isn't new).

            Is responsible for updating the pokedex.
        '''
        self.pokedex[creature.species.pokedex_number] = (1, creature.species)
        
class GameData():
        
    def __init__(self):
        self.is_in_battle = True
        self.battle_data = None
        self.player = None
        
class BattleData():

    def __init__(self, game_data, player_creature, computer_ai, trainer_creature=None, wild_creature=None):
        self.game_data = game_data
        self.player_creature = player_creature
        self.wild_creature = wild_creature
        self.trainer_creature = trainer_creature
        self.computer_ai = computer_ai

    def defending_creature(self):
        return self.trainer_creature if self.trainer_creature != None else self.wild_creature

    def computer_move(self):
        return self.computer_ai.select_move()
            
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
        
class Map():
    
    def __init__(self, name, tiles):
        self.name = name
        self.tiles = tiles