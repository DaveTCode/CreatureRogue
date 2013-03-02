import sys
import sqlite3
from data import Type, Species, TypeChart, StaticGameData, MoveData, Stat, Color, GrowthRate
import settings

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
            growth_rates = self._load_growth_rates(conn)
            xp_lookup = self._load_xp_lookup(conn, growth_rates)
            types = self._load_types(conn)
            type_chart = self._load_type_chart(conn, types)
            moves = self._load_moves(conn, types, stats)
            species = self._load_species(conn, types, colors, stats, growth_rates, moves)
        except sqlite3.Error as e:
            print "An error occurred: ", e.args[0]
            sys.exit(1)
        finally:
            if conn:
                conn.close()
            
        return StaticGameData(species, types, type_chart, moves, stats, colors, growth_rates)

    def _load_stats(self, conn):
        stats = {}
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM stats INNER JOIN stat_names ON stats.id = stat_names.stat_id WHERE local_language_id=' + str(settings.LOCAL_LANGUAGE_ID))
        
        for id, name in cur.fetchall():
            stats[id] = Stat(name)
            
        return stats
        
    def _load_colors(self, conn):
        colors = {}
        cur = conn.cursor()
        cur.execute('SELECT id, name, red, green, blue FROM pokemon_colors INNER JOIN pokemon_color_names ON pokemon_colors.id = pokemon_color_names.pokemon_color_id WHERE local_language_id=' + str(settings.LOCAL_LANGUAGE_ID))
        
        for id, name, red, green, blue in cur.fetchall():
            colors[id] = Color(name, red, green, blue)
            
        return colors
        
    def _load_growth_rates(self, conn):
        growth_rates = {}
        cur = conn.cursor()
        cur.execute('SELECT id, identifier FROM growth_rates')
        
        for id, name in cur.fetchall():
            growth_rates[id] = GrowthRate(name)
            
        return growth_rates
        
    def _load_xp_lookup(self, conn, growth_rates):
        xp_lookup = {}
        cur = conn.cursor()
        cur.execute('SELECT growth_rate_id, level, experience FROM experience ORDER BY growth_rate_id, level')
        
        for growth_rate_id, level, xp in cur.fetchall():
            xp_lookup[growth_rates[growth_rate_id]] = (level, xp)
            
        return xp_lookup
    
    def _load_types(self, conn):
        types = {}
        cur = conn.cursor()
        cur.execute('SELECT types.id, name FROM types INNER JOIN type_names ON type_id = types.id WHERE local_language_id=' + str(settings.LOCAL_LANGUAGE_ID))
        
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
            
        return TypeChart(chart)
    
    def _load_moves(self, conn, types, stats):
        moves = {}
        cur = conn.cursor()
        cur.execute('SELECT * FROM move_data')
        
        for id, name, pp, type_id, power, damage_class_id, accuracy, min_hits, max_hits in cur.fetchall():
            if damage_class_id == 2: # Physical
                attack_stat = stats[2]
                defense_stat = stats[3]
            elif damage_class_id == 3: # Special
                attack_stat = stats[4]
                defense_stat = stats[5]
            else: # Non-damaging
                attack_stat = None
                defense_stat = None
                
            accuracy_stat = stats[7]
            evasion_stat = stats[8]
            
            stat_cur = conn.cursor()
            stat_cur.execute('SELECT stat_id, change FROM move_meta_stat_changes WHERE move_id = ' + str(id))
            
            stat_effects = {stats[stat]: 0 for stat in stats}
            for stat_id, change in stat_cur.fetchall():
                stat_effects[stats[stat_id]] = change
                
            moves[id] = MoveData(name, pp, types[type_id], power, accuracy, min_hits, max_hits, stat_effects, attack_stat, defense_stat, accuracy_stat, evasion_stat)
            
        return moves

    def _load_species(self, conn, types, colors, stats, growth_rates, moves):
        species = {}
        cur = conn.cursor()
        cur.execute('SELECT species_id, creature_id, name, base_experience, color_id, growth_rate_id FROM creature_species_data WHERE pokedex_id = ' + str(settings.POKEDEX_ID) + ' AND local_language_id = ' + str(settings.LOCAL_LANGUAGE_ID))
        
        for species_id, creature_id, name, base_exp, color_id, growth_rate_id in cur.fetchall():
            types_cur = conn.cursor()
            types_cur.execute('SELECT type_id FROM pokemon_types WHERE pokemon_id = ' + str(creature_id))
            species_types = [types[row[0]] for row in types_cur]
            
            stats_cur = conn.cursor()
            stats_cur.execute('SELECT stat_id, base_stat FROM pokemon_stats INNER JOIN stats ON stats.id = pokemon_stats.stat_id WHERE pokemon_id = ' + str(creature_id))
            species_stats = {stats[row[0]]: row[1] for row in stats_cur}
            
            moves_cur = conn.cursor()
            moves_cur.execute('SELECT move_id, level FROM pokemon_moves WHERE pokemon_move_method_id=1 AND pokemon_id=' + str(creature_id) + ' AND version_group_id = ' + str(settings.VERSION_GROUP_ID))
            level_moves = {n:[] for n in range(1,101)}
            for move_id, level in moves_cur.fetchall():
                level_moves[level].append(moves[move_id])
                
            species[species_id] = Species(name, species_types, species_stats, base_exp, growth_rates[growth_rate_id], name[0:1], colors[color_id], level_moves)
            
        return species