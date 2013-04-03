from __future__ import division
import CreatureRogue.libtcodpy as libtcod
import CreatureRogue.settings as settings

class PokedexRenderer():
    
    header_height = 5
    column_width = settings.SCREEN_WIDTH // 4
    column_height = settings.SCREEN_HEIGHT - header_height - 2
    width = settings.SCREEN_WIDTH
    
    def __init__(self, game):
        self.game = game
        self.console = libtcod.console_new(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
        
        self.max_rows = self.column_height - 1
        self.max_columns = len(self.game.static_game_data.species) // self.column_height
        
    def render(self, pokedex, viewing_species, selected_row, selected_column, left_most_column):
        '''
            Major external interface to this class.
            
            Renders the entire of the pokedex passed in to the console which 
            was originally set on the class. Doesn't blit back onto the main
            console as this is the job of the caller.
        '''
        libtcod.console_clear(self.console)
        self._render_lines()
        
        self._render_selection(selected_row, selected_column, left_most_column)
        
        self._render_species(pokedex, left_most_column)
        
        if viewing_species:
            status, species = pokedex[viewing_species]
            
            if status > 0:
                self._render_details_box(species, status)

        return self.console
        
    def _render_lines(self):
        '''
            Render the lines which make up the structure of the pokedex.
        '''
        libtcod.console_set_default_foreground(self.console, settings.POKEDEX_LINE_COLOR)
        libtcod.console_hline(self.console, 0, PokedexRenderer.header_height, PokedexRenderer.width)
        for i in range(PokedexRenderer.column_width, PokedexRenderer.width, PokedexRenderer.column_width):
            libtcod.console_vline(self.console, i, PokedexRenderer.header_height + 1, PokedexRenderer.column_height)
        
    def _render_selection(self, selected_row, selected_column, left_most_column):
        '''
            Render the information on which row, column is currently selected.
        '''
        libtcod.console_set_default_foreground(self.console, settings.POKEDEX_LINE_COLOR)
        libtcod.console_put_char(self.console, (selected_column - left_most_column) * PokedexRenderer.column_width + 19, selected_row + PokedexRenderer.header_height + 1, '<')
        
    def _render_species(self, pokedex, left_most_column):
        '''
            Iterate over all species and put them onto the screen in the 
            appropriate location.
            
            Only displays seen and known species. Each of these can be 
            displayed differently.
        '''
        for pokedex_number in pokedex:
            status, species = pokedex[pokedex_number]
        
            name = "???"
            color = settings.POKEDEX_UNKNOWN_COLOR
            if status == 1:
                name = species.name
                color = settings.POKEDEX_SEEN_COLOR
            elif status == 2:
                name = species.name
                color = settings.POKEDEX_KNOWN_COLOR
    
            column, row = self.calculate_position_of_pokedex_number(pokedex_number - 1, left_most_column)
            
            libtcod.console_set_default_foreground(self.console, color)
            libtcod.console_print(self.console, column * PokedexRenderer.column_width + 1, row + PokedexRenderer.header_height + 1, str(pokedex_number) + ". " + name)

    def _render_details_box(self, species, status):
        '''
            If a pokemon has been selected then this is called to display a 
            box with the specific details as an overlay on top of the pokedex.
        '''
        libtcod.console_set_default_foreground(self.console, settings.POKEDEX_LINE_COLOR)
        libtcod.console_print_frame(self.console, 19, 15, 43, 16) # TODO: Generalise to widths
        
        libtcod.console_print(self.console, 23, 16, u"No. {0.pokedex_number:0=3d}  {0.name}".format(species))
        
        
        if status == 2:
            libtcod.console_print(self.console, 23, 17, u"  {0.genus} Pokemon".format(species))
            libtcod.console_print(self.console, 23, 18, u"Type(s): {0}".format(', '.join(str(t) for t in species.types)))
            libtcod.console_print(self.console, 23, 19, "Height: {0}".format(species.imperial_height_str()))
            libtcod.console_print(self.console, 23, 20, "Weight: {0}".format(species.imperial_weight_str()))
            
            libtcod.console_print_rect(self.console, 20, 22, 41, 14, species.flavor_text)
        elif status == 1:
            libtcod.console_print(self.console, 23, 17, "  ????? Pokemon".format(species))
            libtcod.console_print(self.console, 23, 18, "Type(s): ?????")
            libtcod.console_print(self.console, 23, 19, "Height: ??'??\"")
            libtcod.console_print(self.console, 23, 20, "Weight: ????.? lbs.")
            
    def calculate_position_of_pokedex_number(self, pokedex_number, left_most_column):
        '''
            Given a number in the pokedex this backtracks to find the x, y
            coordinates in the output.
        '''
        return pokedex_number // PokedexRenderer.column_height - left_most_column, pokedex_number % PokedexRenderer.column_height
        
    def calculate_pokedex_number_of_position(self, column, row):
        '''
            Given x, y coordinates in the output table this returns the 
            pokedex number of the creature to be found there.
        '''
        return column * PokedexRenderer.column_height + row + 1