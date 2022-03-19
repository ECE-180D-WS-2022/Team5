import sys
import os
from Ingredients import Ingredients 
import random

class Target_Recipes:
    def __init__(self):
        self.num_max_ingr = 4
        self.base_ingr = [Ingredients("tomato"), 
        Ingredients("lettuce"),
        Ingredients("mushrooms"),
        Ingredients("chicken"), 
        Ingredients("beef"),
        Ingredients("cheese")]   

        self.must_cook_ingr = [Ingredients("chicken"), 
        Ingredients("beef")]


        #self.sandwich_ingr = [Ingredients("bread", 1, 0), Ingredients("lettuce", 2, 0), Ingredients("chicken", 3, 1), Ingredients("2")]

        #self.base_recipe = {'Sandwich': [Ingredients("bread", 1, 0)], 'Soup': [Ingredients("water", 0, 2)], 'Salad': [Ingredients("lettuce", 2, 0)]}
        
        self.recipes_list = {'Sandwich': [Ingredients("bread", 1, 0)],
            'Soup': [Ingredients("water", 0, 2)]}
        
        # self.simple_recipes_list = {'Cooked and Chopped Lettuce': [Ingredients("lettuce", 1, 1)],
        #     'Toasted Cheesy Bread': [Ingredients("cheese", 2, 1), Ingredients("bread", 1, 1)],
        #     'Vegan Salad': [Ingredients("tomato", 3, 0), Ingredients("lettuce", 2, 0)]}
    
    def random_ingr(self, total_recipe, possible_ingr):
        random_ingr = random.choice(possible_ingr)
        random_ingr_name = random_ingr.ingredient_name
        random_cut = random.randint(1,3)
        random_cook = 0
        if (random_ingr in self.must_cook_ingr) or (total_recipe[0].ingredient_name == 'water'):
            random_cook = random.randint(1,3)
        else:
            random_cook = random.randint(0,3)
        return Ingredients(random_ingr_name, random_cut, random_cook)

