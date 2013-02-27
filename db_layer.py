import sys
import sqlite3
from data import Type, Species, TypeChart, StaticGameData, Move, Stat, Color, AttackingMove

class Loader():
    def __init__(self, db_file):
        self.db_file = db_file

    def load_static_data(self):
        '''
            Given a database file we want to load the entire of the static 
            data into the application so that it can be quickly accessed as 
            required.
        '''
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            
            stats = self._load_stats(conn)
            colors = self._load_colors(conn)
            types = self._load_types(conn)
            type_chart = self._load_type_chart(conn, types)
            moves = self._load_moves(conn, types)
            species = self._load_species(conn, types, colors, stats)
        except sqlite3.Error as e:
            print "An error occurred: ", e.args[0]
            sys.exit(1)
        finally:
            if conn:
                conn.close()
            
        return StaticGameData(species, types, type_chart, moves, stats, colors)

    def _load_stats(self, conn):
        stats = {}
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM stats INNER JOIN stat_names ON stats.id = stat_names.stat_id WHERE local_language_id=9')
        
        for id, name in cur.fetchall():
            stats[id] = Stat(name)
            
        return stats
        
    def _load_colors(self, conn):
        colors = {}
        cur = conn.cursor()
        cur.execute('SELECT id, name, red, green, blue FROM pokemon_colors INNER JOIN pokemon_color_names ON pokemon_colors.id = pokemon_color_names.pokemon_color_id WHERE local_language_id=9')
        
        for id, name, red, green, blue in cur.fetchall():
            colors[id] = Color(name, red, green, blue)
            
        return colors
        
    def _load_types(self, conn):
        types = {}
        cur = conn.cursor()
        cur.execute('SELECT types.id, name FROM types INNER JOIN type_names ON type_id = types.id WHERE local_language_id=9') # English languages names only
        
        for id, name in cur.fetchall():
            types[id] = Type(name)
            
        return types
    
    def _load_type_chart(self, conn, types):
        chart = {}
        cur = conn.cursor()
        cur.execute('SELECT damage_type_id, target_type_id, damage_factor FROM type_efficacy')
        
        for damage_type_id, target_type_id, damage_factor in cur.fetchall():
            damage_type = types[damage_type_id]
            target_type = types[target_type_id]
            
            if not damage_type in chart:
                chart[damage_type] = {}
                
            chart[damage_type][target_type] = int(damage_factor)
            
        return chart
    
    # TODO: Only loads attack type moves at the moment.
    def _load_moves(self, conn, types):
        moves = {}
        cur = conn.cursor()
        cur.execute('SELECT moves.id, name, pp, type_id, power FROM moves INNER JOIN move_names ON moves.id = move_names.move_id AND local_language_id = 9 WHERE damage_class_id=2')
        
        for id, name, pp, type_id, power in cur.fetchall():
            moves[id] = AttackingMove(name, pp, types[type_id], power, 'attack', 'defence')
            
        return moves

    def _load_species(self, conn, types, colors, stats):
        species = {}
        cur = conn.cursor()
        cur.execute('SELECT species_id, pokemon_id, name, base_experience, color_id FROM pokemon_species_data WHERE pokedex_id = 1')
        
        for species_id, pokemon_id, name, base_exp, color_id in cur.fetchall():
            types_cur = conn.cursor()
            types_cur.execute('SELECT type_id FROM pokemon_types WHERE pokemon_id = ' + str(pokemon_id))
            species_types = [types[row[0]] for row in types_cur]
            
            stats_cur = conn.cursor()
            stats_cur.execute('SELECT stat_id FROM pokemon_stats INNER JOIN stats ON stats.id = pokemon_stats.stat_id WHERE pokemon_id = ' + str(pokemon_id))
            species_stats = [stats[row[0]] for row in stats_cur]
                
            species[species_id] = Species(name, species_types, species_stats, base_exp, name[0:1], colors[color_id])
            
        return species