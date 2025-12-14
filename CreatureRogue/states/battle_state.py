"""
The battle state is the main state that the game is in when the player is
in a battle.

It is responsible for rendering and input processing.
"""

import collections
import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from CreatureRogue.game import Game
    from CreatureRogue.models.game_data import GameData
    from CreatureRogue.renderer.battle_renderer import (
        BattleRenderer,
        LevelUpRenderer,
        CatchGraphicRenderer,
    )

from tcod import libtcodpy
import tcod

import CreatureRogue.battle_calculations as battle_calculations
import CreatureRogue.data_layer.data as data


class BattleState:
    """
    The main state that the game is in when the player is in a battle.

    Handles input and rendering.
    """

    number_catch_checks = 4
    ms_per_percent_complete = 50

    def __init__(
        self,
        game: "Game",
        game_data: "GameData",
        renderer: "BattleRenderer",
        level_up_renderer: "LevelUpRenderer",
        catch_graphic_renderer: "CatchGraphicRenderer",
    ):
        self.renderer = renderer
        self.level_up_renderer = level_up_renderer
        self.catch_graphic_renderer = catch_graphic_renderer
        self.game_data = game_data
        self.game = game
        self.messages = collections.deque()
        self.end_battle = False
        self.display_level_up = None
        self.selecting_pokeball = False
        self.catching_with_pokeball = None
        self.percent_of_creature_caught = 0
        self.time_started_catching_ms = 0

    def _percent_of_catch_to_display(self):
        """
        Given that we are currently attempting to catch a creature this
        function returns how far through the catch process we are.

        The return value comes as a percent and is maxed at the percent
        caught of the creature (as first calculated).
        """
        return min(
            (libtcodpy.sys_elapsed_milli() - self.time_started_catching_ms)
            / BattleState.ms_per_percent_complete,
            self.percent_of_creature_caught,
        )

    def render(self):
        """
        Render the current state of the battle. Called as many times as
        required by the game loop.
        """
        console = self.renderer.render(
            self.game_data.battle_data, self.messages, self.selecting_pokeball
        )

        if len(self.messages) == 0 and self.display_level_up is not None:
            sub_console = self.level_up_renderer.render(
                self.display_level_up[0].creature, self.display_level_up[1]
            )

            sub_console.blit(console)

        # If we're in the process of catching a creature then there is an
        # extra step which renders the catch graphics on top of the screen.
        if self.catching_with_pokeball:
            percent_to_display = self._percent_of_catch_to_display()
            message = None
            if percent_to_display == self.percent_of_creature_caught:
                message = battle_calculations.get_catch_message(
                    self.percent_of_creature_caught,
                    self.game_data.battle_data.defending_creature(),
                )

            sub_console = self.catch_graphic_renderer.render(
                self.catching_with_pokeball, percent_to_display, message
            )

            sub_console.blit(
                console,
                console.width // 2 - sub_console.width // 2,
                console.height // 2 - sub_console.height // 2,
            )

        # The check to see whether to end the battle is done once in the
        # render function so that we can guarantee that it will get called
        # within a 30fps time frame.
        if (
            len(self.messages) == 0
            and self.display_level_up is None
            and self.end_battle
        ):
            self.game.end_wild_battle()

        return console

    def handle_input(self, event: tcod.event.KeyDown):
        """
        Handle key input when in the battle state. Takes a single key at a
        time but is only called when there is a key press.
        """
        battle_data = self.game_data.battle_data

        if len(self.messages) > 0:
            if (
                event.sym == tcod.event.KeySym.SPACE
                or event.sym == tcod.event.KeySym.RETURN
            ):
                self.messages.popleft()
        elif self.display_level_up:
            if (
                event.sym == tcod.event.KeySym.SPACE
                or event.sym == tcod.event.KeySym.RETURN
            ):
                self.display_level_up = None
        elif self.selecting_pokeball:
            self._selecting_pokeball_input(event)
        elif self.catching_with_pokeball:
            if (
                self._percent_of_catch_to_display() == self.percent_of_creature_caught
                and (
                    event.sym == tcod.event.KeySym.SPACE
                    or event.sym == tcod.event.KeySym.RETURN
                )
            ):
                self._handle_catch_end()
        else:
            if event.sym in (tcod.event.KeySym.C, tcod.event.KeySym.F):
                if (
                    event.sym == tcod.event.KeySym.C
                    and len(self.game_data.player.available_pokeballs()) > 0
                ):
                    self.selecting_pokeball = True
                elif event.sym == tcod.event.KeySym.F:
                    pass
            else:
                move = None
                for key_code, index in [
                    (tcod.event.KeySym.N1, 0),
                    (tcod.event.KeySym.N2, 1),
                    (tcod.event.KeySym.N3, 2),
                    (tcod.event.KeySym.N4, 3),
                ]:
                    if (
                        event.sym == key_code
                        and len(battle_data.player_creature.creature.moves) > index
                    ):
                        move = battle_data.player_creature.creature.moves[index]

                if move is not None:
                    self._handle_move_select(move)

    def _selecting_pokeball_input(self, event: tcod.event.KeyDown):
        """
        Input handler when the sub state is selecting a pokeball.
        """
        if event.sym == tcod.event.KeySym.ESCAPE:
            self.selecting_pokeball = False
        else:
            for pokeball in self.game_data.player.available_pokeballs():
                if event.sym == ord(pokeball.display_char) or event.sym == ord(
                    pokeball.display_char.lower()
                ):
                    self.selecting_pokeball = False
                    self.catching_with_pokeball = pokeball
                    self.time_started_catching_ms = libtcodpy.sys_elapsed_milli()
                    num_checks_passed = battle_calculations.num_catch_checks_passed(
                        self.game_data.battle_data.defending_creature(),
                        pokeball,
                        BattleState.number_catch_checks,
                    )

                    self.percent_of_creature_caught = (
                        100 * num_checks_passed
                    ) // BattleState.number_catch_checks
                    self.game_data.player.use_pokeball(pokeball)
                    break

    def _handle_move_select(self, move):
        """
        Given that the player has selected a move to perform this function
        is called to allow the computer to select a move and then actually
        perform the moves in the correct order.

        It may exit early if a creature faints.
        """
        battle_data = self.game_data.battle_data
        computer_move = battle_data.computer_move()
        speed_stat = self.game.static_game_data.stats[data.SPEED_STAT]

        if battle_data.player_creature.stat_value(
            speed_stat
        ) > battle_data.defending_creature().stat_value(speed_stat):
            first_move = (
                move,
                battle_data.player_creature,
                battle_data.defending_creature(),
            )
            second_move = (
                computer_move,
                battle_data.defending_creature(),
                battle_data.player_creature,
            )
        elif battle_data.player_creature.stat_value(
            speed_stat
        ) < battle_data.defending_creature().stat_value(speed_stat):
            first_move = (
                computer_move,
                battle_data.defending_creature(),
                battle_data.player_creature,
            )
            second_move = (
                move,
                battle_data.player_creature,
                battle_data.defending_creature(),
            )
        else:
            if random.randint(0, 1) == 0:
                first_move = (
                    move,
                    battle_data.player_creature,
                    battle_data.defending_creature(),
                )
                second_move = (
                    computer_move,
                    battle_data.defending_creature(),
                    battle_data.player_creature,
                )
            else:
                first_move = (
                    computer_move,
                    battle_data.defending_creature(),
                    battle_data.player_creature,
                )
                second_move = (
                    move,
                    battle_data.player_creature,
                    battle_data.defending_creature(),
                )

        for move, aggressor, defender in [first_move, second_move]:
            # The move can actually be None if there were no valid
            # moves to select from.
            if move:
                messages = battle_calculations.perform_move(
                    move, aggressor, defender, self.game.static_game_data
                )

                for message in messages:
                    self.messages.append(message)

                # Check the state of the creatures, we don't end the battle
                # immediately because we still want to process any
                # remaining messages.
                #
                # We do need to break out though so that the fainted
                # creature can't have it's turn.
                if defender.creature.fainted:
                    self._creature_fainted(aggressor, defender)

                if aggressor.creature.fainted or defender.creature.fainted:
                    self.end_battle = True
                    break

    def _creature_fainted(self, aggressor, defender):
        """
        Called when a creature faints during battle. Used to add experience
        to the winner and check for level ups.
        """
        xp_given = defender.creature.xp_given(1, False)

        old_level = aggressor.creature.level
        messages = aggressor.creature.add_xp(
            self.game.static_game_data.xp_lookup, xp_given
        )

        for message in messages:
            self.messages.append(message)

        if old_level != aggressor.creature.level:
            self.display_level_up = (aggressor, old_level)

    def _handle_catch_end(self):
        """
        Called when the catch process completes, either because the
        creature was caught or because it escaped.

        May switch out of the battle state.
        """
        if self.percent_of_creature_caught == 100:
            self.game.catch_creature(
                self.game_data.battle_data.defending_creature().creature
            )
        else:
            self.catching_with_pokeball = None
            self.percent_of_creature_caught = 0
            self.time_started_catching_ms = 0
