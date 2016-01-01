"""
    A move is a single action that a creature can take during a battle.
"""
from __future__ import division
import random
from CreatureRogue.data_layer import data

class Move():
    def __init__(self, move_data):
        self.move_data = move_data
        self.pp = self.move_data.max_pp