from map_renderer import *

tiles = [[MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE), MapCell(EXIT_NORTH, None), MapCell(EXIT_NORTH, None), MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(LONG_GRASS), MapCell(LONG_GRASS), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE), MapCell(LONG_GRASS), MapCell(LONG_GRASS), MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE), MapCell(LONG_GRASS), MapCell(LONG_GRASS), MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)],
         [MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE), MapCell(EXIT_SOUTH, None), MapCell(EXIT_SOUTH, None), MapCell(TREE), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(GRASS), MapCell(TREE)]]