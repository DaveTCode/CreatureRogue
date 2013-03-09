from __future__ import division
from game import Game
import settings

if __name__ == "__main__":
    game = Game(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.TITLE, settings.FONT)
    game.init()

    
    while True:
        location_area_id = int(raw_input('Which location do you want to load (by id)? '))
    
        location_area = game.static_game_data.location_areas[location_area_id]

        encounters = {}
        for i in range(0, 10000):
            encounter = location_area.get_encounter()
            if not encounter in encounters:
                encounters[encounter] = 0
            
            encounters[encounter] += 1

        for encounter in encounters:
            print "{0} - {1}".format(encounter, str(encounters[encounter]  * 100 / 10000))

        if raw_input('Exit?') == 'y':
            break