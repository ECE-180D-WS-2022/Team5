import sys
import os
from Ingredients import *
from Target_Recipes import *
import random

T_R = Target_Recipes()
num_extra_ingr = random.randint(1,3)
print("number of extra ingredients")
print(num_extra_ingr)
print("==========")
target_recipes_list = list(T_R.recipes_list.items())
target_recipe = random.choice(target_recipes_list) # results in a list that contains: name, ingredients list
total_recipe = target_recipe[1]
possible_ingr = T_R.base_ingr

i = 0
skip = False
while i < num_extra_ingr:
    rand_ingr = T_R.random_ingr(total_recipe, possible_ingr)
    for a in range(len(total_recipe)):
        if rand_ingr.ingredient_name in total_recipe[a].ingredient_name:
            possible_ingr.remove(Ingredients(rand_ingr.ingredient_name))
            skip = True
            break
    if skip == True:
        skip = False
        break
    print(rand_ingr.ingredient_name)
    print(rand_ingr.cut_state)
    print(rand_ingr.cook_state)
    total_recipe.append(rand_ingr)
    i += 1
print("==========")
print("Recipe name: " + target_recipe[0])
print("Random ingredients chosen:")
for b in range(len(total_recipe)):
    print(total_recipe[b].ingredient_name, total_recipe[b].cut_state, total_recipe[b].cook_state)

print("==========")
set_of_base_ingr = []
for a in range(len(total_recipe)):
    set_of_base_ingr.append(Ingredients(total_recipe[a].ingredient_name))

for b in range(len(set_of_base_ingr)):
    print(set_of_base_ingr[b].ingredient_name, set_of_base_ingr[b].cut_state, set_of_base_ingr[b].cook_state)