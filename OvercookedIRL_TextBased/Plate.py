import sys
import os

class Plate:
    def __init__(self, plate_number, state):
        self.plate_number = plate_number # to help identify which plate is which
        self.state = state # 0: empty, 1: not empty
        self.ingredients = [] # will hold all the ingredients 