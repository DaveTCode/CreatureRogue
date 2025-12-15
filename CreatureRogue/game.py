"""
The game module contains the main game loop as well as any code which
doesn't yet have a sensible home.

Use Game.create() to instantiate a fully initialized game.
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass

import tcod

import CreatureRogue.creature_creator as creature_creator
import CreatureRogue.data_layer.data as data
import CreatureRogue.data_layer.db_layer as db_layer
import CreatureRogue.settings as settings
from CreatureRogue.battle_ai import RandomMoveAi
from CreatureRogue.models.battle_creature import BattleCreature
from CreatureRogue.models.battle_data import BattleData
from CreatureRogue.models.game_data import GameData
from CreatureRogue.renderer.battle_renderer import (
    BattleRenderer,
    CatchGraphicRenderer,
    LevelUpRenderer,
)
from CreatureRogue.renderer.game_menu_renderer import GameMenuRenderer
from CreatureRogue.renderer.map_renderer import MapRenderer
from CreatureRogue.renderer.pokedex_renderer import PokedexRenderer
from CreatureRogue.states.battle_state import BattleState
from CreatureRogue.states.game_menu_state import InGameMenuState
from CreatureRogue.states.map_state import MapState
from CreatureRogue.states.pokedex_state import PokedexState


@dataclass
class GameConfig:
    """Configuration for creating a Game instance."""

    screen_width: int
    screen_height: int
    title: str
    font: str


class Game:
    def __init__(
        self,
        config: GameConfig,
        static_game_data: data.StaticGameData,
        game_data: GameData,
        battle_renderer: BattleRenderer,
        map_renderer: MapRenderer,
        pokedex_renderer: PokedexRenderer,
        level_up_renderer: LevelUpRenderer,
        game_menu_renderer: GameMenuRenderer,
        catch_graphic_renderer: CatchGraphicRenderer,
    ):
        self.config = config
        self.static_game_data = static_game_data
        self.game_data = game_data
        self.battle_renderer = battle_renderer
        self.map_renderer = map_renderer
        self.pokedex_renderer = pokedex_renderer
        self.level_up_renderer = level_up_renderer
        self.game_menu_renderer = game_menu_renderer
        self.catch_graphic_renderer = catch_graphic_renderer
        self.state = MapState(self, self.game_data, self.map_renderer)

    @classmethod
    def create(
        cls,
        screen_width: int = settings.SCREEN_WIDTH,
        screen_height: int = settings.SCREEN_HEIGHT,
        title: str = settings.TITLE,
        font: str = settings.FONT,
    ) -> Game:
        """
        Factory method to create a fully initialized Game instance.

        This loads all static data from the database and creates all renderers.
        """
        config = GameConfig(screen_width, screen_height, title, font)

        # Load static game data
        location_area_rectangles = data.load_location_area_rects(
            settings.LOCATION_AREA_RECTS_FILE
        )
        static_game_data = db_layer.Loader(settings.DB_FILE).load_static_data(location_area_rectangles)

        # Create game data
        game_data = GameData()

        # Create a temporary game reference for renderers that need it
        # We'll create a partial game first, then set up state
        temp_game = object.__new__(cls)
        temp_game.config = config
        temp_game.static_game_data = static_game_data
        temp_game.game_data = game_data

        # Create renderers
        battle_renderer = BattleRenderer(temp_game)
        map_renderer = MapRenderer()
        pokedex_renderer = PokedexRenderer(temp_game)
        level_up_renderer = LevelUpRenderer(temp_game)
        game_menu_renderer = GameMenuRenderer(temp_game)
        catch_graphic_renderer = CatchGraphicRenderer(temp_game)

        # Now create the full game with all dependencies
        game = cls(
            config=config,
            static_game_data=static_game_data,
            game_data=game_data,
            battle_renderer=battle_renderer,
            map_renderer=map_renderer,
            pokedex_renderer=pokedex_renderer,
            level_up_renderer=level_up_renderer,
            game_menu_renderer=game_menu_renderer,
            catch_graphic_renderer=catch_graphic_renderer,
        )

        # Update renderer references to point to the real game
        battle_renderer.game = game
        pokedex_renderer.game = game
        level_up_renderer.game = game
        game_menu_renderer.game = game
        catch_graphic_renderer.game = game

        return game

    @property
    def screen_width(self) -> int:
        return self.config.screen_width

    @property
    def screen_height(self) -> int:
        return self.config.screen_height

    @property
    def title(self) -> str:
        return self.config.title

    @property
    def font(self) -> str:
        return self.config.font

    def game_loop(self):
        """
        The game loop runs until the user closes the window manually. All
        game logic and rendering is done here.
        """
        console = tcod.console.Console(self.screen_width, self.screen_height)
        with tcod.context.new(
            columns=self.screen_width,
            rows=self.screen_height,
            title=self.title,
            tileset=tcod.tileset.load_tilesheet(
                self.font, 16, 16, tcod.tileset.CHARMAP_TCOD
            ),
        ) as context:
            while True:
                console.draw_frame(
                    0,
                    0,
                    self.screen_width,
                    self.screen_height,
                    fg=settings.FOREGROUND_COLOR,
                )

                if self.state is not None:
                    output_console = self.state.render()
                    output_console.blit(
                        console, 0, 0, self.screen_width, self.screen_height, 0, 0
                    )

                context.present(console)

                for event in tcod.event.wait():
                    context.convert_event(
                        event
                    )  # Sets tile coordinates for mouse events.

                    match event:
                        case tcod.event.KeyDown():
                            if self.state is not None:
                                self.state.handle_input(event)
                        case tcod.event.Quit():
                            raise SystemExit

        self.end_game()

    ###########################################################################
    # Below here there are function which transition between game states. This
    # will inevitably move somewhere else at some point so I'm separating it
    # out.
    #
    # In fact it will probably turn into a state machine.
    ###########################################################################

    def start_wild_battle(self):
        # Choose a pokemon to fight
        x, y = self.game_data.player.coords
        location_area_id = (
            self.static_game_data.location_area_rects.get_location_area_by_position(
                x, y
            )
        )

        if location_area_id is not None:
            encounter = self.static_game_data.location_areas[
                location_area_id
            ].get_encounter()

            level = random.randint(encounter.min_level, encounter.max_level)
            wild_creature = creature_creator.create_wild_creature(
                self.static_game_data, encounter.species, level
            )
            self.game_data.player.encounter_creature(wild_creature)

            self.game_data.battle_data = BattleData(
                self.game_data,
                BattleCreature(
                    self.game_data.player.creatures[0], self.static_game_data
                ),
                RandomMoveAi(BattleCreature(wild_creature, self.static_game_data)),
                wild_creature=BattleCreature(wild_creature, self.static_game_data),
            )

            self.state = BattleState(
                self,
                self.game_data,
                self.battle_renderer,
                self.level_up_renderer,
                self.catch_graphic_renderer,
            )

    def catch_creature(self, creature):
        self.game_data.player.catch_creature(creature)
        self.game_data.battle_data = None
        self.state = MapState(self, self.game_data, self.map_renderer)

    def end_wild_battle(self):
        self.game_data.battle_data = None
        self.state = MapState(self, self.game_data, self.map_renderer)

    def load_pokedex(self):
        self.state = PokedexState(self, self.game_data, self.pokedex_renderer)

    def close_pokedex(self):
        self.state = InGameMenuState(
            self, self.game_data, self.map_renderer, self.game_menu_renderer
        )

    def open_menu(self):
        self.state = InGameMenuState(
            self, self.game_data, self.map_renderer, self.game_menu_renderer
        )

    def close_menu(self):
        self.state = MapState(self, self.game_data, self.map_renderer)

    @staticmethod
    def end_game():
        sys.exit(0)


def main():
    """Entry point for the game when installed as a package."""
    game = Game.create()
    game.game_loop()
