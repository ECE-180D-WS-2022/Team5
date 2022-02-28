import sys
import os

class Ingredients:
    def __init__(self, ingredient_name, cut_state, cook_state):
        self.ingredient_name = ingredient_name
        self.cut_state = cut_state # 0: raw, 1: prepared once, 2: prepared twice, 3: prepared thrice, ....
        self.cook_state = cook_state
        self.prepare_stations = ["Cutting Station", "Stove Station"] # station where ingredient must be prepared in

    # note about __eq__ from this website: https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes
    def __eq__(self, other):
        if not isinstance(other, Ingredients):
            return NotImplemented

        return (self.ingredient_name == other.ingredient_name) and (self.cut_state == other.cut_state) and (self.cook_state == other.cook_state)
