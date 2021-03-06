# text based implementation of Overcooked IRL single player mode only

import sys
import os
import random

from numpy import isin
from Station_Manager import Station_Manager
from Player import Player
from Plate import Plate
from Ingredients import *
from Target_Recipes import *
import random
import speech_recognition as sr
import copy

current_score = 0
plate_num = 0 # first plate number starts at 0
valid_actions = ['put down', 'pick up']
stations = ["Cutting Station", "Stove Station", "Ingredients Station", "Submit Station", "Share Station", "Plate Station", "Counter"]
station_num = ["1", "2", "3", "4", "5", "6", "7"]
station_manager = Station_Manager()
completed_current_recipe = True

T_R = Target_Recipes()
num_extra_ingr = random.randint(1,3)
target_recipes_list = list(T_R.recipes_list.items())
set_of_base_ingr = []
valid_ingredients_names = []

def main():
    os.system('cls') # use cls for PowerShell; may need to change for other output terminals
    print("Welcome to OvercookedIRL!")
    print("Instructions: If you see different option names with numbers in front, only type the number and press Enter.")
    print("If you see only different option names without numbers in front, type the exact option name and press Enter.")
    print("Any other instructions will be given otherwise.\n")
    print ("1.) Start")
    print ("2.) Load")
    print ("3.) Exit")
    option = input("-> ")
    if option == "1":
        start()
    elif option == "2":
        pass
    elif option == "3":
        sys.exit()
    else: 
        main()

def start():
    os.system('cls')
    print("Hello, what is your name (please type in your name): ")
    option = input("-> ")
    global PlayerIG
    PlayerIG = Player(option)
    pick_station()

def start2():
    os.system('cls')
    global completed_current_recipe, target_recipe, station_manager, current_score, set_of_base_ingr, target_recipe_li
    if completed_current_recipe:
        target_recipe_li = random.choice(target_recipes_list) # results in a list that contains: name, ingredients list
        target_recipe = target_recipe_li[1]
        possible_ingr = T_R.base_ingr
        i = 0
        skip = False
        while i < num_extra_ingr:
            rand_ingr = T_R.random_ingr(target_recipe, possible_ingr)
            for a in range(len(target_recipe)):
                if rand_ingr.ingredient_name in target_recipe[a].ingredient_name:
                    possible_ingr.remove(Ingredients(rand_ingr.ingredient_name))
                    skip = True
                    break
            if skip == True:
                skip = False
                break
            target_recipe.append(rand_ingr)
            i += 1

        set_of_base_ingr = []
        for a in range(len(target_recipe)):
            set_of_base_ingr.append(Ingredients(target_recipe[a].ingredient_name))
        i = 0
        while (i < len(set_of_base_ingr)):
            valid_ingredients_names.append(set_of_base_ingr[i].ingredient_name)
            i += 1
        completed_current_recipe = False
        
    print ("Name: %s" % PlayerIG.name)
    print("Current Score: %s" % current_score)
    print("Target Recipe: %s" % target_recipe_li[0])
    if PlayerIG.inventory:
        if isinstance(PlayerIG.inventory[0], Ingredients):
            print("Inventory: %s, cut_state: %s, cook_state: %s" % (PlayerIG.inventory[0].ingredient_name, PlayerIG.inventory[0].cut_state, PlayerIG.inventory[0].cook_state))
        elif isinstance(PlayerIG.inventory[0], Plate):
            if not PlayerIG.inventory[0].ingredients:
                print("Inventory: Plate %s with: Nothing" % PlayerIG.inventory[0].plate_number)
            else:
                print("Inventory: Plate %s with:" % PlayerIG.inventory[0].plate_number)
                plate_ingredients = PlayerIG.inventory[0].ingredients
                i = 0
                while i < len(plate_ingredients):
                    print("\t%s, cut_state: %s, cook_state: %s" % (plate_ingredients[i].ingredient_name, plate_ingredients[i].cut_state, plate_ingredients[i].cook_state))
                    i += 1
    else:
        print("Inventory: Empty")
    print("Location: %s" % PlayerIG.location)
    n = 0
    while n < len(station_manager.stations):
        current_station = station_manager.stations[n]
        if PlayerIG.location == current_station.station_name:
            if not current_station.ingredient:
                print("Location Ingredient: Empty\n")
            else:
                if isinstance(current_station.ingredient, Ingredients):
                    print("Location Ingredient: %s, cut_state: %s, cook_state: %s\n" % (current_station.ingredient.ingredient_name, current_station.ingredient.cut_state, current_station.ingredient.cook_state))
                elif isinstance(current_station.ingredient, Plate): 
                    plate_ingredients = current_station.ingredient.ingredients
                    if not current_station.ingredient:
                        print("Location Ingredient: Plate %s with: Nothing" % current_station.ingredient.plate_number)
                    else:
                        i = 0
                        print("Location Ingredient: Plate %s with: " % current_station.ingredient.plate_number)
                        while i < len(plate_ingredients):
                            print("\t%s, cut_state: %s, cook_state: %s" % (plate_ingredients[i].ingredient_name, plate_ingredients[i].cut_state, plate_ingredients[i].cook_state))
                            i += 1
            break
        n += 1
    

    print("What do you want to do?")
    print ("1.) Move")
    print ("2.) Pick Up")
    print ("3.) Put Down")
    print ("4.) Action")
    print ("5.) Submit ")
    print ("6.) Trash Inventory")
    print ("7.) Trash Location")
    print ("8.) Look at Recipe")
    # option = input("-> ")
    input("Press Enter to begin speaking...")
    option = listen()
    if option == "move":
        pick_station()
    elif option == "pick up":
        pickup()
    elif option == "put down":
        putdown()
    elif option == "action":
        action()
    elif option == "submit":
        submit()
    elif option == "trash inventory":
        trash_inv()
    elif option == "trash location":
        trash_loc_ingr()
    elif option == "look":
        view_recipe()
    else:
        start2()

def view_recipe():
    global target_recipe_li, target_recipe
    os.system('cls')
    print("Recipe name: " + target_recipe_li[0])
    for b in range(len(target_recipe)):
        print(target_recipe[b].ingredient_name, target_recipe[b].cut_state, target_recipe[b].cook_state)
    input("Press Enter to continue.")
    start2()

def pick_station(): 
    os.system('cls')
    print ("Which station do you want to go to?")    
    print ("1.) Cutting Station")
    print ("2.) Stove Station")
    print ("3.) Ingredients Station")
    print ("4.) Submit Station")
    print ("5.) Share Station")
    print ("6.) Plate Station")
    print ("7.) Counter")
    option = input("-> ")
    if option in station_num:
        station_int = int(option) - 1
        move(stations[station_int])
    else: 
        start2()

def move(station_name):
    PlayerIG.location = station_name
    start2()

def action():
    os.system('cls')
    global station_manager
    global PlayerIG
    if (PlayerIG.location == "Ingredients Station") and not PlayerIG.inventory:
        print ("What ingredient do you want?")
        print(*valid_ingredients_names, sep = ", ")
        input("Press Enter to begin speaking...")
        option = listen()
        # option = input("-> ")
        if option in valid_ingredients_names:
            n = 0
            while n < len(set_of_base_ingr): # is there a better way to access a single attribute of a list of objects?
                if option == set_of_base_ingr[n].ingredient_name:
                    PlayerIG.inventory.append(copy.copy(set_of_base_ingr[n])) # want new object that is a copy; don't want to reference the same exact object to use
                    break
                n += 1
            start2()
        else: 
            start2()
    elif (PlayerIG.location == "Ingredients Station") and PlayerIG.inventory:
        print("Your inventory is full.")
        print("Do you want to replace your item in your inventory?")
        print("1.) Yes")
        print("2.) No")
        option = input("-> ")
        if option == "1":
            PlayerIG.inventory.clear()
            print(*valid_ingredients_names, sep = ", ")
            option = input("-> ")
            if option in valid_ingredients_names:
                n = 0
                while n < len(set_of_base_ingr):
                    if option == set_of_base_ingr[n].ingredient_name:
                        PlayerIG.inventory.append(set_of_base_ingr[n])
                        break
                    n += 1
                start2()
            else: 
                start2()
        elif option == "2":
            start2()
        else:
            action()
    elif PlayerIG.location in ["Share Station", "Submit Station"]: # these have other specific functions
        start2()
    else: # if player is at Cutting or Stove Station
        n = 0
        while n < len(station_manager.stations):
            if PlayerIG.location == station_manager.stations[n].station_name:
                if station_manager.stations[n].ingredient: # if the station has an ingredient, process the item
                    if PlayerIG.location == "Cutting Station":
                        station_manager.stations[n].ingredient.cut_state += 1
                    else: # at stove station
                        station_manager.stations[n].ingredient.cook_state += 1
                    break
                else:
                    start2()
            n += 1
        start2()

# NOT for picking up ingredients at INGREDIENT STATION; pickup anything else elsewhere
def pickup():
    os.system('cls')
    global station_manager
    global PlayerIG

    if not PlayerIG.inventory: # if player inventory is empty
        if PlayerIG.location == "Plate Station":
            global plate_num
            PlayerIG.inventory.append(Plate(plate_num))
            plate_num += 1
            start2()
        elif PlayerIG.location == "Share Station":
            pass
        elif PlayerIG.location == "Ingredients Station":
            start2()
        else:
            n = 0
            while n < len(station_manager.stations):
                if (PlayerIG.location == station_manager.stations[n].station_name):
                    if (station_manager.stations[n].busy == 1): # if station has something
                        if (isinstance(station_manager.stations[n].ingredient, Ingredients)): # if item at the station is an ingredient
                            if (station_manager.stations[n].ingredient.cut_state == 0) and (station_manager.stations[n].ingredient.cook_state == 0): #if station item is an ingredient that is RAW, add it to inventory
                                PlayerIG.inventory.append(station_manager.stations[n].ingredient)
                                station_manager.stations[n].busy = 0
                                station_manager.stations[n].ingredient = None
                                break
                            else: # if station item is an ingredient that has been PREPARED, cannot add to an empty inventory
                                print("You need a plate to pick up PREPARED ingredients")
                                input("Press enter to continue")
                                break
                        else: # if item at the station is not an ingredient, it must be a plate and thus add it to the empty inventory
                            PlayerIG.inventory.append(station_manager.stations[n].ingredient)
                            station_manager.stations[n].busy = 0
                            station_manager.stations[n].ingredient = None
                            break
                    else: # if there is nothing at the station
                        break   
                n += 1
            start2()
    else: # player inventory is full
        if PlayerIG.location in ["Plate Station", "Ingredients Station", "Submit Station"]:
            start2()
        elif PlayerIG.location == "Share Station": # add when share station is necessary
            pass
        else:
            if (isinstance(PlayerIG.inventory[0], Plate)): 
                n = 0
                while n < len(station_manager.stations):
                    if (PlayerIG.location == station_manager.stations[n].station_name):
                        if (station_manager.stations[n].busy == 1): # if there is something at the station
                            if (isinstance(station_manager.stations[n].ingredient, Plate)): # if the item is a plate, cannot pick up because inventory is full
                                break
                            else: # if the item is an ingredient
                                if (station_manager.stations[n].ingredient.cut_state == 0) and (station_manager.stations[n].ingredient.cook_state == 0): # if ingredient is RAW
                                    print("You cannot add RAW ingredients to your plate")
                                    input("Press enter to continue")
                                    break
                                else: # if ingredient is PREPARED, add that ingredient to player's plate
                                    PlayerIG.inventory[0].ingredients.append(station_manager.stations[n].ingredient)
                                    station_manager.stations[n].busy = 0
                                    station_manager.stations[n].ingredient = None


                        else: # if there is nothing at the station
                            break
                    n += 1
            else: # if player inventory is an ingredient, don't do anything
                print("Inventory is full with an ingredient; cannot pick up anything")
                input("Press enter to continue")
            start2()

def putdown():
    os.system('cls')
    global station_manager
    global PlayerIG
    if not PlayerIG.inventory: # if player inventory is empty, don't do anything
        start2()
    else:
        if (PlayerIG.location == "Ingredients Station") or (PlayerIG.location == "Submit Station"):
            print("Cannot put down items here")
            input("Press Enter to continue")
            start2()
        item = PlayerIG.inventory[0]
        n = 0
        while n < len(station_manager.stations):
            if (station_manager.stations[n].station_name == "Counter") and (PlayerIG.location == "Counter"): # at the counter, you can place raw ingredients or plates (only plates can have prepared ingredients on it anyway) on the counter
                if (station_manager.stations[n].busy == 0):
                    station_manager.stations[n].busy = 1
                    station_manager.stations[n].ingredient = item
                    PlayerIG.inventory.clear()
                    break
            if (PlayerIG.location == station_manager.stations[n].station_name):
                if (station_manager.stations[n].busy == 0):
                    if (isinstance(item, Ingredients)): # if player's inventory is an ingredient (RAW or PREPARED), put it onto the station
                        station_manager.stations[n].busy = 1
                        station_manager.stations[n].ingredient = item
                        PlayerIG.inventory.clear()
                        break
                    else: # if player's inventory is a Plate
                        if not item.ingredients: # if the plate has no ingredients on it, do nothing
                            break
                        else: # if the plate has ingredients on it, ask which one the player wants to put down
                            print("Which ingredient do you want to put down? Please put down the name:")
                            i = 0
                            i_list = []
                            while i < len(item.ingredients):
                                print("\t%s, cut_state: %s, cook_state: %s" % (item.ingredients[i].ingredient_name, item.ingredients[i].cut_state, item.ingredients[i].cook_state))
                                i_list.append(item.ingredients[i].ingredient_name)
                                i += 1
                            option = input("-> ")
                            if option in i_list:
                                index = i_list.index(option)
                                station_manager.stations[n].busy = 1
                                station_manager.stations[n].ingredient = item.ingredients[index]
                                item.ingredients.pop(index)
                                break
                            else:
                                break
                      
            n += 1
        start2()



# only applies to Submit Station
def submit():
    os.system('cls')
    global completed_current_recipe, current_score
    if PlayerIG.location == "Submit Station":
        if not PlayerIG.inventory:
            start2()
        else:
            if isinstance(PlayerIG.inventory[0], Plate):
                print("%s has submitted plate number: %s" % (PlayerIG.name, PlayerIG.inventory[0].plate_number))
                if PlayerIG.inventory[0].ingredients == target_recipe[1]:
                    print("Good job!")
                    current_score += 1
                else:
                    print("WRONG RECIPE")
                    current_score -= 1
                PlayerIG.inventory.clear()
                completed_current_recipe = True
                input("Press Enter to continue")
                start2()     
            else:
                start2()
    else:
        start2()

def trash_inv():
    os.system('cls')
    global PlayerIG
    print("Do you want to clear your inventory?")
    print("1.) Yes")
    print("2.) No")
    option = input("-> ")
    if option == "1":
        PlayerIG.inventory.clear()
        start2()
    elif option == "2":
        start2()
    else: 
        trash_inv()

def trash_loc_ingr(): # trash location ingredient
    os.system('cls')
    global station_manager, PlayerIG
    print("Do you want to clear the location ingredient?")
    print("1.) Yes")
    print("2.) No")
    option = input("-> ")
    if option == "1":
        n = 0
        while n < len(station_manager.stations):
            if PlayerIG.location == station_manager.stations[n].station_name:
                station_manager.stations[n].busy = 0
                station_manager.stations[n].ingredient = None
            n += 1
        start2()
    elif option == "2":
        start2()
    else: 
        trash_loc_ingr()

def inspect_recipe():
    os.system('cls')
    global target_recipe
    target_recipe_ingr = target_recipe[1]
    print ("Recipe for %s:" % target_recipe[0])
    n = 0
    while n < len(target_recipe_ingr):
        print("\t%s, cut_state: %s, cook_state: %s" % (target_recipe_ingr[n].ingredient_name, target_recipe_ingr[n].cut_state, target_recipe_ingr[n].cook_state))
        n += 1    
    input("Press Enter to go back")
    start2()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        recog_word = r.recognize_google(audio)
        return recog_word
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


main()