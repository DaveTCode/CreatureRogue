"""
The game module contains the main game loop as well as any code which
doesn't yet have a sensible home.

Correct access is via calling init, load_static_data then game_loop
"""

import random
import sys

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


class Game:
    def __init__(self, screen_width: int, screen_height: int, title: str, font: str):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        self.font = font
        self.static_game_data = None

        self.state = None
        self.game_data = None
        self.battle_renderer = None
        self.map_renderer = None
        self.pokedex_renderer = None
        self.level_up_renderer = None
        self.game_menu_renderer = None
        self.catch_graphic_renderer = None

    def load_static_data(self):
        """
        This is required all over and must be called before init is called
        to create the renderers.
        """
        self.static_game_data = db_layer.Loader(settings.DB_FILE).load_static_data()
        self.static_game_data.location_area_rects = data.load_location_area_rects(
            settings.LOCATION_AREA_RECTS_FILE
        )

    def init(self):
        """
        Set up the libtcod window with the parameters given to the game.
        This must be called before the game loop is run.
        """
        if self.static_game_data is None:
            print("You must load the static game data before calling init")
            sys.exit(1)

        self.game_data = GameData()
        # TODO: Need to set up the player object here or it will be none in the game data.

        self.battle_renderer = BattleRenderer(self)
        self.map_renderer = MapRenderer()
        self.pokedex_renderer = PokedexRenderer(self)
        self.level_up_renderer = LevelUpRenderer(self)
        self.game_menu_renderer = GameMenuRenderer(self)
        self.catch_graphic_renderer = CatchGraphicRenderer(self)

        self.state = MapState(self, self.game_data, self.map_renderer)

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
    game = Game(
        settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT
    )
    game.load_static_data()
    game.init()
    game.game_loop()
