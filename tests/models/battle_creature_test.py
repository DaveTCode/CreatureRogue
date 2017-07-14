import CreatureRogue.creature_creator as creature_creator
import CreatureRogue.settings as settings
from CreatureRogue.data_layer.data import ATTACK_STAT
from CreatureRogue.data_layer.db_layer import Loader
from CreatureRogue.models.creature import Creature
from CreatureRogue.models.battle_creature import BattleCreature


loader = Loader(settings.DB_FILE)
static_game_data = loader.load_static_data()


def test_string_blank_name():
    creature = Creature(species=static_game_data.species[1], level=1, nickname=None, trainer=None,
                        individual_values=creature_creator.random_stat_values(static_game_data.stats, 1, 15),
                        effort_values=creature_creator.zero_stat_values(static_game_data.stats),
                        current_xp=1, was_traded=False, moves=[])
    battle_creature = BattleCreature(creature=creature, static_game_data=static_game_data)
    assert "Wild Bulbasaur" == str(battle_creature)


def test_stat_value_function():
    creature = Creature(species=static_game_data.species[1], level=1, nickname=None, trainer=None,
                        individual_values=creature_creator.random_stat_values(static_game_data.stats, 1, 15),
                        effort_values=creature_creator.zero_stat_values(static_game_data.stats),
                        current_xp=1, was_traded=False, moves=[])
    battle_creature = BattleCreature(creature=creature, static_game_data=static_game_data)
    assert 6.0 == battle_creature.stat_value(static_game_data.stats[ATTACK_STAT])
    battle_creature.adjust_stat_adjusts(static_game_data.stats[ATTACK_STAT], 1)
    assert 6.0 * 1.5 == battle_creature.stat_value(static_game_data.stats[ATTACK_STAT])  # Multiply default by 1.5


def test_stat_value_positive_capping():
    creature = Creature(species=static_game_data.species[1], level=1, nickname=None, trainer=None,
                        individual_values=creature_creator.random_stat_values(static_game_data.stats, 1, 15),
                        effort_values=creature_creator.zero_stat_values(static_game_data.stats),
                        current_xp=1, was_traded=False, moves=[])
    battle_creature = BattleCreature(creature=creature, static_game_data=static_game_data)
    battle_creature.adjust_stat_adjusts(static_game_data.stats[ATTACK_STAT], 6)
    assert 6.0 * 4.0 == battle_creature.stat_value(static_game_data.stats[ATTACK_STAT])
    assert 0 == battle_creature.adjust_stat_adjusts(static_game_data.stats[ATTACK_STAT], 1)
    assert 6.0 * 4.0 == battle_creature.stat_value(static_game_data.stats[ATTACK_STAT])  # Should still be the same


def test_stat_value_negative_capping():
    creature = Creature(species=static_game_data.species[1], level=1, nickname=None, trainer=None,
                        individual_values=creature_creator.random_stat_values(static_game_data.stats, 1, 15),
                        effort_values=creature_creator.zero_stat_values(static_game_data.stats),
                        current_xp=1, was_traded=False, moves=[])
    battle_creature = BattleCreature(creature=creature, static_game_data=static_game_data)
    battle_creature.adjust_stat_adjusts(static_game_data.stats[ATTACK_STAT], -6)
    assert 6.0 / 4.0 == battle_creature.stat_value(static_game_data.stats[ATTACK_STAT])
    assert 0 == battle_creature.adjust_stat_adjusts(static_game_data.stats[ATTACK_STAT], -1)
    assert 6.0 / 4.0 == battle_creature.stat_value(static_game_data.stats[ATTACK_STAT])  # Should still be the same


def test_modified_catch_rate():
    creature = Creature(species=static_game_data.species[1], level=1, nickname=None, trainer=None,
                        individual_values=creature_creator.random_stat_values(static_game_data.stats, 1, 15),
                        effort_values=creature_creator.zero_stat_values(static_game_data.stats),
                        current_xp=1, was_traded=False, moves=[])
    battle_creature = BattleCreature(creature=creature, static_game_data=static_game_data)
    assert 15.0 == battle_creature.modified_catch_rate(static_game_data.pokeballs[1])
