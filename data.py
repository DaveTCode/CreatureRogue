import sqlite3

class StaticGameData():
    def __init__(self):
        self.species = None
        self.types = None
        self.type_chart = None
        self.moves = None

    def load(self, database_file):
        '''
            Given a database file we want to load the entire of the static 
            data into the application so that it can be quickly accessed as 
            required.
        '''
        try:
            conn = sqlite3.connect(database_file)
            self.types = self._load_types(conn)
            self.type_chart = self._load_type_chart(conn)
            self.moves = self._load_moves(conn)
        except sqlite3.Error as e:
            print "An error occurred: ", e.args[0]
        finally:
            conn.close()
        
    def _load_types(self, db_connection):

class Species():
    
    def __init__(self, name, types, base_hp, base_xp_yield, display_character, display_color):
        self.name = name
        self.types = types
        self.base_hp = base_hp
        self.base_xp_yield = base_xp_yield
        self.display_character = display_character
        self.display_color = display_color
        
class Type():
    
    def __init__(self, name):
        self.name = name
        
class TypeChart():
    def __init__(self, chart):
        self.chart = chart
        
    def damage_modifier(type_1, type_2):
        return self.chart[type_1][type_2]
        
class Move():
    
    def __init__(self, name, max_pp, type):
        self.name = name
        self.max_pp = max_pp
        self.type = type

class AttackingMove(Move):
    
    def __init__(self, name, max_pp, type, base_attack, attack_stat, defence_stat):
        super(AttackingMove, self).__init__(name, max_pp, type)
        self.base_attack = base_attack
        self.attack_stat = attack_stat
        self.defence_stat = defence_stat
        
    def damage_calculation(self, attacking_creature, defending_creature, type_chart):
        '''
            To calculate the damage that a move does we need to know which
            creature is performing the move and which is defending it.
            
            The return value for this is the hitpoint delta.
        '''
        attack_stat_value = attacking_creature.stats[self.attack_stat]
        defence_stat_value = defending_creature.stats[self.defence_stat]
        
        # Modifiers
        critical_modifier = 2 if random.uniform(0, 100) < 6.25 else 1 # TODO: Incomplete - should use items and check whether this is a high critical move etc
        same_type_attack_bonus = 1.5 if self.type in attacking_creature.types else 1
        type_modifier = 1
        for type in defending_creature.types:
            type_modifier = type_modifier * type_chart.damage_modifier(self.type, type)
            
        modifier = same_type_attack_bonus * type_modifier * critical_modifier # TODO: Incomplete - Ignoring weather effects and other bits
        
        return math.floor((((2 * attacking_creature.level + 10) / 250) * (attack_stat_value / defence_stat_value) * self.base_attack + 2) * modifier)