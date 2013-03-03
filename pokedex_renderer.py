from __future__ import division
import libtcodpy as libtcod
import settings

class PokedexRenderer():
    
    header_height = 5
    column_width = settings.SCREEN_WIDTH // 4
    column_height = settings.SCREEN_HEIGHT - header_height - 2
    width = settings.SCREEN_WIDTH
    
    def __init__(self, static_game_data, console, pokedex):
        self.console = console
        self.static_game_data = static_game_data
        self.selected_column = 0
        self.selected_row = 0
        self.viewing_species = None
        self.left_most_column = 0
        
        self.max_rows = self.column_height - 1
        self.max_columns = len(self.static_game_data.species) // self.column_height
        self.pokedex = pokedex

    def displaying_species(self):
        return self.viewing_species != None
        
    def display_selected(self):
        pokedex_id = self._calculate_pokedex_number_of_position(self.selected_column, self.selected_row)
    
        if self.pokedex[pokedex_id][0] > 0:
            self.viewing_species = pokedex_id
        
    def close_display(self):
        self.viewing_species = None
        
    def shift_row(self, delta):
        '''
            Changes which row is currently selected. Bounds the row by the 
            maximum number so that the row index is never out of the 
            valid range.
        '''
        self.selected_row = self.selected_row + delta
        if self.selected_row < 0:
            self.selected_row = 0
        elif self.selected_row > self.max_rows:
            self.selected_row = self.max_rows
    
    def shift_column(self, delta):
        '''
            Changes which column is currently selected. Bounds the column by 
            the maximum number so that the row index is never out of the 
            valid range.
        '''
        self.selected_column = self.selected_column + delta
        if self.selected_column < 0:
            self.selected_column = 0
        elif self.selected_column > self.max_columns:
            self.selected_column = self.max_columns
            
        while self.selected_column - self.left_most_column >= 4:
            self.left_most_column += 1
        while self.selected_column < self.left_most_column:
            self.left_most_column -= 1
        
    def render(self):
        '''
            Major external interface to this class.
            
            Renders the entire of the pokedex passed in to the console which 
            was originally set on the class. Doesn't blit back onto the main
            console as this is the job of the caller.
        '''
        self._render_lines()
        
        self._render_selection()
        
        self._render_species(self.pokedex)
        
        if self.viewing_species:
            status, species = self.pokedex[self.viewing_species]
            
            if status > 0:
                self._render_details_box(species, status)
        
    def _render_lines(self):
        '''
            Render the lines which make up the structure of the pokedex.
        '''
        libtcod.console_set_default_foreground(self.console, settings.POKEDEX_LINE_COLOR)
        libtcod.console_hline(self.console, 0, PokedexRenderer.header_height, PokedexRenderer.width)
        for i in range(PokedexRenderer.column_width, PokedexRenderer.width, PokedexRenderer.column_width):
            libtcod.console_vline(self.console, i, PokedexRenderer.header_height + 1, PokedexRenderer.column_height)
        
    def _render_selection(self):
        '''
            Render the information on which row, column is currently selected.
        '''
        libtcod.console_set_default_foreground(self.console, settings.POKEDEX_LINE_COLOR)
        libtcod.console_put_char(self.console, (self.selected_column - self.left_most_column) * PokedexRenderer.column_width + 19, self.selected_row + PokedexRenderer.header_height + 1, '<')
        
    def _render_species(self, pokedex):
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
    
            column, row = self._calculate_position_of_pokedex_number(pokedex_number - 1)
            
            libtcod.console_set_default_foreground(self.console, color)
            libtcod.console_print(self.console, column * PokedexRenderer.column_width + 1, row + PokedexRenderer.header_height + 1, str(pokedex_number) + ". " + name)

    def _render_details_box(self, species, status):
        '''
            If a pokemon has been selected then this is called to display a 
            box with the specific details as an overlay on top of the pokedex.
        '''
        libtcod.console_set_default_foreground(self.console, settings.POKEDEX_LINE_COLOR)
        libtcod.console_print_frame(self.console, 19, 15, 43, 16) # TODO: Generalise to widths
        
        libtcod.console_print(self.console, 23, 16, 'No. {0.pokedex_number:0=3d}  {0.name}'.format(species))
        
        
        if status == 2:
            libtcod.console_print(self.console, 23, 17, '  {0.genus} Pokemon'.format(species))
            libtcod.console_print(self.console, 23, 18, 'Type(s): {0}'.format(', '.join(str(t) for t in species.types)))
            libtcod.console_print(self.console, 23, 19, 'Height: {0}'.format(species.imperial_height_str()))
            libtcod.console_print(self.console, 23, 20, 'Weight: {0}'.format(species.imperial_weight_str()))
            
            libtcod.console_print_rect(self.console, 20, 22, 41, 14, species.flavor_text)
        elif status == 1:
            libtcod.console_print(self.console, 23, 17, '  ????? Pokemon'.format(species))
            libtcod.console_print(self.console, 23, 18, 'Type(s): ?????')
            libtcod.console_print(self.console, 23, 19, 'Height: ??\'??"')
            libtcod.console_print(self.console, 23, 20, 'Weight: ????.? lbs.')
            
    def _calculate_position_of_pokedex_number(self, pokedex_number):
        return pokedex_number // PokedexRenderer.column_height - self.left_most_column, pokedex_number % PokedexRenderer.column_height
        
    def _calculate_pokedex_number_of_position(self, column, row):
        return column * PokedexRenderer.column_height + row + 1