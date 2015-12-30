"""
Main module. Provides command line run access.
"""

import CreatureRogue.settings as settings
from CreatureRogue.game import Game

if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.load_static_data()
    game.init()
    game.game_loop()
