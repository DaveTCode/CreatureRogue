import libtcodpy as libtcod

class PokedexState():

    def __init__(self, game, game_data, pokedex_renderer):
        self.game = game_data
        self.game_data = game_data
        self.pokedex_renderer = pokedex_renderer

    def handle_input(self, key):
        if self.pokedex_renderer.displaying_species():
            if key.vk == libtcod.KEY_ESCAPE:
                self.pokedex_renderer.close_display()
        else:
            if key.vk == libtcod.KEY_LEFT:
                self.pokedex_renderer.shift_column(-1)
            elif key.vk == libtcod.KEY_RIGHT:
                self.pokedex_renderer.shift_column(1)
            elif key.vk == libtcod.KEY_UP:
                self.pokedex_renderer.shift_row(-1)
            elif key.vk == libtcod.KEY_DOWN:
                self.pokedex_renderer.shift_row(1)
            elif key.vk == libtcod.KEY_ENTER:
                self.pokedex_renderer.display_selected()

    def render(self):
        self.pokedex_renderer.render()