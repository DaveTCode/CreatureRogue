'''
    The main game state when the player is viewing the pokedex.

    Handles input and rendering and allows the player to return to the main
    game state.
'''
import CreatureRogue.libtcodpy as libtcod

class PokedexState():

    def __init__(self, game, game_data, pokedex_renderer):
        self.game = game
        self.game_data = game_data
        self.pokedex_renderer = pokedex_renderer

        self.selected_column = 0
        self.selected_row = 0
        self.viewing_species = None
        self.left_most_column = 0

    def displaying_species(self):
        '''
            Returns True if the species details box is displayed otherwise 
            false.
        '''
        return self.viewing_species != None
        
    def display_selected(self):
        '''
            Display the currently selected species (as specified by 
            self.selected_row, self.selected_column).
        '''
        pokedex_id = self.pokedex_renderer.calculate_pokedex_number_of_position(self.selected_column, self.selected_row)
    
        if len(self.game_data.player.pokedex) > pokedex_id and self.game_data.player.pokedex[pokedex_id][0] > 0:
            self.viewing_species = pokedex_id
        
    def close_display(self):
        '''
            External interface to indicate that we are to stop viewing the 
            current species.
        '''
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
        elif self.selected_row > self.pokedex_renderer.max_rows:
            self.selected_row = self.pokedex_renderer.max_rows
    
    def shift_column(self, delta):
        '''
            Changes which column is currently selected. Bounds the column by 
            the maximum number so that the row index is never out of the 
            valid range.
        '''
        self.selected_column = self.selected_column + delta
        if self.selected_column < 0:
            self.selected_column = 0
        elif self.selected_column > self.pokedex_renderer.max_columns:
            self.selected_column = self.pokedex_renderer.max_columns
            
        while self.selected_column - self.left_most_column >= 4:
            self.left_most_column += 1
        while self.selected_column < self.left_most_column:
            self.left_most_column -= 1

    def handle_input(self, key):
        '''
            Handles a single key press when viewing the pokedex.
        '''
        if self.displaying_species():
            if key.vk == libtcod.KEY_ESCAPE:
                self.close_display()
        else:
            if key.vk == libtcod.KEY_LEFT:
                self.shift_column(-1)
            elif key.vk == libtcod.KEY_RIGHT:
                self.shift_column(1)
            elif key.vk == libtcod.KEY_UP:
                self.shift_row(-1)
            elif key.vk == libtcod.KEY_DOWN:
                self.shift_row(1)
            elif key.vk == libtcod.KEY_ENTER:
                self.display_selected()
            elif key.vk == libtcod.KEY_ESCAPE:
                self.game.close_pokedex()

    def render(self):
        '''
            Passes control off to the pokedex renderer to display the current 
            pokedex state.
        '''
        return self.pokedex_renderer.render(self.game_data.player.pokedex, 
                                            self.viewing_species, 
                                            self.selected_row, 
                                            self.selected_column, 
                                            self.left_most_column)