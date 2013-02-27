from game import Game
import settings

if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.init()
    game.game_loop()