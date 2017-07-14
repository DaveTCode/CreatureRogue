import CreatureRogue.creature_creator as creature_creator
import CreatureRogue.settings as settings
from CreatureRogue.data_layer.db_layer import Loader
from CreatureRogue.models.creature import Creature
from CreatureRogue.models.battle_creature import BattleCreature


def test_string_blank_name():
    loader = Loader(settings.DB_FILE)
    static_game_data = loader.load_static_data()
    creature = Creature(species=static_game_data.species[1], level=1, nickname=None, trainer=None,
                        individual_values=creature_creator.random_stat_values(static_game_data.stats, 1, 15),
                        effort_values=creature_creator.zero_stat_values(static_game_data.stats),
                        current_xp=1, was_traded=False, moves=[])
    battle_creature = BattleCreature(creature=creature, static_game_data=static_game_data)
    assert "Wild Bulbasaur" == str(battle_creature)
