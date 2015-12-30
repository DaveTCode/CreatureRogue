"""
    The db layer module is used to load information from the static database
    data into a static data object. Acts as an ORM.
"""
import sqlite3
import sys

import CreatureRogue.data.data as data
import tcod as libtcod
import CreatureRogue.settings as settings


class Loader:
    def __init__(self, db_file):
        self.db_file = db_file

    def load_static_data(self):
        """
            Given a database file we want to load the entire of the static 
            data into the application so that it can be quickly accessed as 
            required.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)

            # XP
            growth_rates = self._load_growth_rates(conn)
            xp_lookup = self._load_xp_lookup(conn, growth_rates)

            # Types
            types = self._load_types(conn)
            type_chart = self._load_type_chart(conn, types)

            # Stats
            stats = self._load_stats(conn)

            # Ailments
            ailments = self._load_ailments(conn)

            # Moves
            move_targets = self._load_move_targets(conn)
            moves = self._load_moves(conn, types, stats, move_targets, ailments)

            # Pokeballs
            pokeballs = self._load_pokeballs(conn)

            # Species
            colors = self._load_colors(conn)
            species = self._load_species(conn, types, colors, stats, growth_rates, moves)

            # Regions/Areas
            regions = self._load_regions(conn)
            locations = self._load_locations(conn, regions)
            location_areas = self._load_location_areas(conn, locations, species)
        except sqlite3.Error as err:
            print("An error occurred: ", err.args[0])  # TODO - Convert to logger
            sys.exit(1)
        finally:
            if conn:
                conn.close()

        return data.StaticGameData(species, types, type_chart, moves, stats, colors, growth_rates, move_targets,
                                   regions, locations, location_areas, xp_lookup, pokeballs, ailments)

    def _load_ailments(self, conn):
        ailments = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT id, name FROM move_meta_ailments INNER JOIN move_meta_ailment_names ON move_meta_ailments.id = move_meta_ailment_names.move_meta_ailment_id WHERE local_language_id={0}'.format(
                settings.LOCAL_LANGUAGE_ID))

        for ailment_id, name in cur.fetchall():
            ailments[ailment_id] = data.Ailment(ailment_id, name)

        return ailments

    def _load_stats(self, conn):
        stats = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT id, name, short_name FROM stats INNER JOIN stat_names ON stats.id = stat_names.stat_id WHERE local_language_id={0}'.format(
                settings.LOCAL_LANGUAGE_ID))

        for stat_id, name, short_name in cur.fetchall():
            stats[stat_id] = data.Stat(name, short_name)

        return stats

    def _load_colors(self, conn):
        colors = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT id, name, red, green, blue FROM pokemon_colors INNER JOIN pokemon_color_names ON pokemon_colors.id = pokemon_color_names.pokemon_color_id WHERE local_language_id=' + str(
                settings.LOCAL_LANGUAGE_ID))

        for color_id, name, red, green, blue in cur.fetchall():
            colors[color_id] = data.Color(name, red, green, blue)

        return colors

    def _load_growth_rates(self, conn):
        growth_rates = {}
        cur = conn.cursor()
        cur.execute('SELECT id, identifier FROM growth_rates')

        for gr_id, name in cur.fetchall():
            growth_rates[gr_id] = data.GrowthRate(name)

        return growth_rates

    def _load_xp_lookup(self, conn, growth_rates):
        xp_lookup = {growth_rates[growth_rate_id]: {} for growth_rate_id in growth_rates}
        cur = conn.cursor()
        cur.execute('SELECT growth_rate_id, level, experience FROM experience ORDER BY growth_rate_id, level')

        for growth_rate_id, level, xp in cur.fetchall():
            xp_lookup[growth_rates[growth_rate_id]][level] = xp

        return data.XpLookup(xp_lookup)

    def _load_pokeballs(self, conn):
        pokeballs = {}
        cur = conn.cursor()
        cur.execute('SELECT id, name, catch_rate, top_color, bottom_color, display_char FROM pokeballs')

        for pokeball_id, name, catch_rate, top_color, bottom_color, display_char in cur.fetchall():
            r_top, g_top, b_top = [int(a) for a in top_color.split(',')]
            r_bottom, g_bottom, b_bottom = [int(a) for a in bottom_color.split(',')]

            pokeballs[pokeball_id] = data.Pokeball(pokeball_id, name, catch_rate, libtcod.Color(r_top, g_top, b_top),
                                                   libtcod.Color(r_bottom, g_bottom, b_bottom), display_char)

        return pokeballs

    def _load_move_targets(self, conn):
        targets = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT id, identifier, name, description FROM move_targets INNER JOIN move_target_prose ON id = move_target_id WHERE local_language_id={0}'.format(
                settings.LOCAL_LANGUAGE_ID))

        for mt_id, identifier, name, description in cur.fetchall():
            targets[mt_id] = data.MoveTarget(identifier, name, description)

        return targets

    def _load_types(self, conn):
        types = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT types.id, name FROM types INNER JOIN type_names ON type_id = types.id WHERE local_language_id={0}'.format(
                settings.LOCAL_LANGUAGE_ID))

        for type_id, name in cur.fetchall():
            types[type_id] = data.Type(name)

        return types

    def _load_type_chart(self, conn, types):
        chart = {}
        cur = conn.cursor()
        cur.execute('SELECT damage_type_id, target_type_id, damage_factor FROM type_efficacy')

        for damage_type_id, target_type_id, damage_factor in cur.fetchall():
            damage_type = types[damage_type_id]
            target_type = types[target_type_id]

            if damage_type not in chart:
                chart[damage_type] = {}

            chart[damage_type][target_type] = int(damage_factor)

        return data.TypeChart(chart)

    def _load_moves(self, conn, types, stats, move_targets, ailments):
        moves = {}
        cur = conn.cursor()
        cur.execute('SELECT * FROM move_data')

        for move_id, name, pp, type_id, power, damage_class_id, accuracy, min_hits, max_hits, target_id, ailment_id in cur.fetchall():
            if damage_class_id == 2:  # Physical
                attack_stat = stats[2]
                defense_stat = stats[3]
            elif damage_class_id == 3:  # Special
                attack_stat = stats[4]
                defense_stat = stats[5]
            else:  # Non-damaging
                attack_stat = None
                defense_stat = None

            accuracy_stat = stats[7]
            evasion_stat = stats[8]

            stat_cur = conn.cursor()
            stat_cur.execute('SELECT stat_id, change FROM move_meta_stat_changes WHERE move_id = {0}'.format(move_id))

            stat_effects = {stats[stat]: 0 for stat in stats}
            for stat_id, change in stat_cur.fetchall():
                stat_effects[stats[stat_id]] = change

            moves[move_id] = data.MoveData(name, pp, types[type_id], power, accuracy, min_hits, max_hits, stat_effects,
                                           attack_stat, defense_stat, accuracy_stat, evasion_stat,
                                           move_targets[target_id], ailments[ailment_id])

        return moves

    def _load_species(self, conn, types, colors, stats, growth_rates, moves):
        species = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT species_id, creature_id, pokedex_number, name, height, weight, base_experience, color_id, growth_rate_id, flavor_text, genus, capture_rate FROM creature_species_data WHERE pokedex_id = {0} AND local_language_id = {1}'.format(
                settings.POKEDEX_ID, settings.LOCAL_LANGUAGE_ID))

        for species_id, creature_id, pokedex_number, name, height, weight, base_exp, color_id, growth_rate_id, flavor_text, genus, capture_rate in cur.fetchall():
            types_cur = conn.cursor()
            types_cur.execute('SELECT type_id FROM pokemon_types WHERE pokemon_id = {0}'.format(creature_id))
            species_types = [types[row[0]] for row in types_cur]

            stats_cur = conn.cursor()
            stats_cur.execute(
                'SELECT stat_id, base_stat FROM pokemon_stats INNER JOIN stats ON stats.id = pokemon_stats.stat_id WHERE pokemon_id = {0}'.format(
                    creature_id))
            species_stats = {stats[row[0]]: row[1] for row in stats_cur}
            species_stats[stats[data.EVASION_STAT]] = 1
            species_stats[stats[data.ACCURACY_STAT]] = 1

            moves_cur = conn.cursor()
            moves_cur.execute(
                'SELECT move_id, level FROM pokemon_moves WHERE pokemon_move_method_id=1 AND pokemon_id={0} AND version_group_id = {1}'.format(
                    creature_id, settings.VERSION_GROUP_ID))
            level_moves = {n: [] for n in range(1, 101)}
            for move_id, level in moves_cur.fetchall():
                level_moves[level].append(moves[move_id])

            species[species_id] = data.Species(pokedex_number, name, height, weight, species_types, species_stats,
                                               base_exp, growth_rates[growth_rate_id], name[0:1], colors[color_id],
                                               level_moves, flavor_text, genus, capture_rate)

        return species

    def _load_regions(self, conn):
        regions = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT id, identifier, name FROM regions INNER JOIN region_names ON regions.id = region_names.region_id WHERE local_language_id={0}'.format(
                settings.LOCAL_LANGUAGE_ID))

        for region_id, identifier, name in cur.fetchall():
            regions[region_id] = data.Region(identifier, name)

        return regions

    def _load_locations(self, conn, regions):
        locations = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT id, identifier, name, region_id FROM locations INNER JOIN location_names ON locations.id = location_names.location_id WHERE local_language_id={0} AND NOT region_id IS NULL'.format(
                settings.LOCAL_LANGUAGE_ID))

        for location_id, identifier, name, region_id in cur.fetchall():
            locations[location_id] = data.Location(identifier, name, regions[region_id])

        return locations

    def _load_location_areas(self, conn, locations, species):
        location_areas = {}
        cur = conn.cursor()
        cur.execute(
            'SELECT location_areas.id, location_areas.identifier, location_area_prose.name, location_areas.location_id FROM location_areas INNER JOIN location_area_prose ON location_areas.id = location_area_prose.location_area_id WHERE NOT location_areas.location_id IS NULL AND local_language_id={0}'.format(
                settings.LOCAL_LANGUAGE_ID))

        for area_id, identifier, name, location_id in cur.fetchall():
            rate_cur = conn.cursor()
            rate_cur.execute(
                'SELECT encounter_method_id, rate FROM location_area_encounter_rates WHERE version_id = (SELECT MAX(version_id) FROM location_area_encounter_rates WHERE location_area_id = {0}) AND location_area_id = {0}'.format(
                    area_id))

            walk_encounter_rate = 0
            for method_id, rate in rate_cur.fetchall():
                if method_id == 1:
                    walk_encounter_rate = rate

            enc_cur = conn.cursor()
            enc_cur.execute(
                'SELECT species_id, MIN(min_level), MAX(max_level), MAX(rarity), encounter_method_id FROM encounters INNER JOIN pokemon on pokemon_id = pokemon.id INNER JOIN encounter_slots ON encounter_slots.id = encounters.encounter_slot_id WHERE location_area_id = {0} GROUP BY pokemon_id, encounter_method_id'.format(
                    area_id))

            walk_encs = []
            for species_id, min_level, max_level, rarity, method_id in enc_cur.fetchall():
                if method_id == 1:
                    walk_encs.append(data.Encounter(species[species_id], min_level, max_level, rarity))

            location_areas[area_id] = data.LocationArea(identifier, name, locations[location_id], walk_encs, walk_encounter_rate)

        return location_areas
