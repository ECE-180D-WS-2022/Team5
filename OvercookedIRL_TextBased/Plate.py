import sys
import os

class Plate:
    def __init__(self, plate_number):
        self.plate_number = plate_number # to help identify which plate is which
        self.ingredients = [] # will hold all the ingredients
    
    def __eq__(self, other):
        if not isinstance(other, Plate):
            return NotImplemented

        return self.ingredients == other.ingredients