import sys
import os
from Ingredients import Ingredients 

class Target_Recipes:
    def __init__(self):
        self.base_ingredients = [Ingredients("tomato", 0, 0), 
        Ingredients("cheese", 0, 0), 
        Ingredients("bread", 0, 0), 
        Ingredients("beef", 0, 0), 
        Ingredients("lettuce", 0, 0)]
        self.recipes_list = {'Classic Sandwich': [Ingredients("tomato", 2, 0), Ingredients("cheese", 3, 0), Ingredients("bread", 1, 0), Ingredients("beef", 1, 1), Ingredients("lettuce", 1, 0)],
            'Cooked and Chopped Lettuce': [Ingredients("lettuce", 1, 1)],
            'Toasted Cheesy Bread': [Ingredients("cheese", 2, 1), Ingredients("bread", 1, 1)]}
        self.simple_recipes_list = {'Cooked and Chopped Lettuce': [Ingredients("lettuce", 1, 1)],
            'Toasted Cheesy Bread': [Ingredients("cheese", 2, 1), Ingredients("bread", 1, 1)],
            'Vegan Salad': [Ingredients("tomato", 3, 0), Ingredients("lettuce", 2, 0)]}
