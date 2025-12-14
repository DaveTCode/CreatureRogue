"""
All calculations done during a battle are stored in this file. This is
essentially all of the game logic for battles.
"""

import random

import CreatureRogue.data_layer.data as data
from CreatureRogue.data_layer.data import StaticGameData
from CreatureRogue.data_layer.pokeball import Pokeball
from CreatureRogue.data_layer.stat import Stat
from CreatureRogue.models.battle_creature import BattleCreature
from CreatureRogue.models.move import Move


def perform_move(
    move: Move,
    attacking_creature: BattleCreature,
    defending_creature: BattleCreature,
    static_game_data: StaticGameData,
):
    """
    Performs the move by the attacking creature on the defending_creature.

    This can change both the attacking creature, the defending creature and
    cause messages to be returned.
    """
    messages = []

    if move.pp <= 0:
        messages.append(f"Not enough points to perform {move.move_data.name}")
    else:
        messages.append(
            f"{attacking_creature.creature.in_battle_name()} used {move.move_data.name}"
        )
        move.pp -= 1

        # Check if the move misses
        if not hit_calculation(move, attacking_creature, defending_creature):
            messages.append(f"{attacking_creature.creature.in_battle_name()}'s attack missed!")
        else:
            # TODO: Missing the "specific-move" target and only considering 1v1 battles.
            target = None
            if move.move_data.target.identifier in [
                "user",
                "users-field",
                "user-or-ally",
                "entire-field",
            ]:
                target = attacking_creature
            if move.move_data.target.identifier in [
                "selected-pokemon",
                "random-opponent",
                "all-other-pokemon",
                "opponents-field",
                "all-opponents",
                "entire-field",
            ]:
                target = defending_creature

            if target:
                if move.move_data.damage_move():
                    new_messages, hp_loss = damage_calculation(
                        move, attacking_creature, target, static_game_data.type_chart
                    )

                    messages.extend(new_messages)

                    hp_stat = static_game_data.stat(data.HP_STAT)
                    target.creature.adjust_stat(hp_stat, hp_loss)

                    if target.stat_value(hp_stat) <= 0:
                        target.creature.fainted = True
                        messages.append(f"{target.creature.in_battle_name()} fainted!")

                if move.move_data.stat_change_move():
                    for stat, value in move.move_data.stat_changes.items():
                        if value != 0:
                            adjust_amount = target.adjust_stat_adjusts(stat, value)

                            messages.append(
                                get_stat_change_message(move, target, adjust_amount, stat)
                            )

    return messages


def hit_calculation(
    move: Move, attacking_creature: BattleCreature, defending_creature: BattleCreature
) -> bool:
    """
    Determines whether the move will hit the defending creature.
    This is based on a random check.
    """
    if move.move_data.base_accuracy:
        return random.random() < (
            move.move_data.base_accuracy
            / 100
            * (
                attacking_creature.stat_value(move.move_data.accuracy_stat)
                / defending_creature.stat_value(move.move_data.evasion_stat)
            )
        )

    return False


def damage_calculation(
    move: Move,
    attacking_creature: BattleCreature,
    defending_creature: BattleCreature,
    type_chart,
) -> tuple[list[str], int]:
    """
    To calculate the damage that a move does we need to know which
    creature is performing the move and which is defending it.

    The return value for this is the hitpoint delta.
    """
    attack_stat_value = attacking_creature.stat_value(move.move_data.attack_stat)
    defence_stat_value = defending_creature.stat_value(move.move_data.defence_stat)

    # Modifiers
    critical_modifier = (
        2 if random.uniform(0, 100) < 6.25 else 1
    )  # TODO: Incomplete - should use items and check whether this is a high critical move etc
    same_type_attack_bonus = (
        1.5 if move.move_data.type in attacking_creature.creature.species.types else 1
    )
    type_modifier = 1
    for defending_type in defending_creature.creature.species.types:
        type_modifier = (
            type_modifier * type_chart.damage_modifier(move.move_data.type, defending_type) / 100
        )

    modifier = (
        same_type_attack_bonus * type_modifier * critical_modifier
    )  # TODO: Incomplete - Ignoring weather effects and other bits

    messages = []
    if critical_modifier > 1:
        messages.append("Critical hit!")
    if type_modifier == 0:
        messages.append("The attack had no effect!")
    elif type_modifier < 0.9:
        messages.append("The attack was not very effective")
    elif type_modifier > 1.1:
        messages.append("The attack was super effective!")

    return messages, int(
        (
            ((2 * attacking_creature.creature.level + 10) / 250)
            * (attack_stat_value / defence_stat_value)
            * move.move_data.base_attack
            + 2
        )
        * modifier
    )


def num_catch_checks_passed(creature: BattleCreature, pokeball: Pokeball, num_shakes: int):
    """
    Catching a creature is based on a catch rate (modified from the
    creatures base catch rate), the ball used and a set of random
    checks.

    This function determines how many random checks are passed.
    """
    a = creature.modified_catch_rate(pokeball)
    b = 65535 * (a / 255) ** (1 / 4)

    for i in range(num_shakes):
        if random.randint(0, 65535) > b:
            return i

    return num_shakes


def get_catch_message(percent_complete, creature) -> str:
    """
    Used to generate the display message when we try to catch a creature.
    """
    if percent_complete <= 25:
        return "Not even close!"
    if percent_complete <= 50:
        return "Well, that could have gone worse"
    if percent_complete <= 70:
        return "I'll totally get it next time!"
    if percent_complete < 100:
        return "Damn...so close!"
    return f"Gotcha! {creature.creature.in_battle_name()} was caught"


def get_stat_change_message(
    move: Move, target: BattleCreature, stat_change: int, stat: Stat
) -> str:
    """
    Creates the message which is displayed when a creatures stats change.
    """
    if (
        stat_change == 0
        and move.move_data.stat_changes[stat] != 0
        and not move.move_data.damage_move()
    ):
        direction = "higher" if move.move_data.stat_changes[stat] > 0 else "lower"
        return f"{target.creature.in_battle_name()}'s {stat.name} won't go any {direction}!"
    if stat_change == 1:
        return f"{target.creature.in_battle_name()}'s {stat.name} rose!"
    if stat_change == 2:
        return f"{target.creature.in_battle_name()}'s {stat.name} sharply rose!"
    if stat_change > 2:
        return f"{target.creature.in_battle_name()}'s {stat.name} rose drastically!"
    if stat_change == -1:
        return f"{target.creature.in_battle_name()}'s {stat.name} fell!"
    if stat_change == -2:
        return f"{target.creature.in_battle_name()}'s {stat.name} harshly fell!"
    if stat_change < -2:
        return f"{target.creature.in_battle_name()}'s {stat.name} severely fell!"

    return ""
