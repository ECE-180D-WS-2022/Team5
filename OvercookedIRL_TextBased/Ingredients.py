import sys
import os

class Ingredients:
    def __init__(self, ingredient_name, state = 0, prepare_station = None):
        self.ingredient_name = ingredient_name
        self.state = state # 0: raw, 1: prepared once, 2: prepared twice, 3: prepared thrice, ....
        self.prepare_station = prepare_station # station where ingredient must be prepared in