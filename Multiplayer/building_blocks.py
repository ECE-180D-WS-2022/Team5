# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:43:02 2022

@author: Kellen Cheng
"""

# Import Statements
import sys
import copy
import socket
import pickle

# Game Parameters
HEADER = 4096
stations = ["Cutting Board", "Stove", "Ingredients Stand", 
            "Plates Cupboard", "Submission Countertop", "Share Station"]

###############################################################################
'''
Action Codes (AKA first entry in the list of data we send to the server):
    -1   -> Do nothing (AKA error code or performed invalid action)
    0    -> Register
    1    -> Move player
    2    -> Pick up item
    3    -> Put down item
    4    -> Perform Gesture/Speech
    5    -> Submit dish
    6    -> Destroy player inventory
    7    -> Destroy station items
    8    -> Exit the game
    
Additional Gameplay Notes:
    - Cannot have both a separated plate and ingredient at a station at the
    same time. They only coexist when the ingredient is on the plate.
    - Our inventory may only contain one item (plate OR ingredient), however do
    note that it can contain a plate that is NOT EMPTY (i.e. has food on it)
'''
###############################################################################

# Function: Game logic driver
def game(client_socket):
    print("############### Welcome to Overcooked IRL ###############")
    
    # Store local copies of any player parameters
    current = None # Local copy of the name of the current player location
    # inventory = 0 # Local copy of inventory size
    
    # Register a new player
    register(client_socket, header=HEADER)
    
    # At the start, first move to a station
    current = move(client_socket, header=HEADER)
    status = pickle.loads(client_socket.recv(HEADER))
    
    # Print initial game state
    if (status != None):
            print("Player location:", str(status[0]))
            print("Player inventory:", str(status[1]))
            print("Pantry inventory:", str(status[2]))
            print("Target recipe:", str(status[3]))
    
    # Begin game logic
    while True:
        current = action(client_socket, header=HEADER, loc=current)
        
        # Retrieve game state and print logistics after every action
        status = pickle.loads(client_socket.recv(HEADER))
        print("_________________________________________________")
        
        if (status != None):
            print("Player location:", str(status[0]))
            print("Player inventory:", str(status[1]))
            print("Pantry inventory:", str(status[2]))
            print("Target recipe:", str(status[3]))
        
        
   
# Function: Register a game player
def register(client_socket, header=HEADER): # ACTION = 0
    name = input("Please enter your player's name:\n")
    client_socket.send(pickle.dumps([0, name])) # Send information to be stored
    
# Function: Move stations as a player
def move(client_socket, header=HEADER): # ACTION = 1
    print("Select a station from one of the following below:")
    dest = int(input("(1) Cutting Board (2) Stove (3) Ingredients Stand" \
                 " (4) Plates Cupboard (5) Submission Countertop" \
                     " (6) Share Station\n"))
    
    client_socket.send(pickle.dumps([1, dest])) # Send information to be stored
    return stations[dest - 1]

# Function: Complete an action
def action(client_socket, header=HEADER, loc=None): # ACTION = VARIABLE
    print("Select an option from one of the following below:")
    dest = int(input("(1) Move (2) Pick Up (3) Put Down" \
                 " (4) Gesture/Speech (5) Submit (6) Trash Inventory"\
                     " (7) Trash Station (8) Exit \n"))
    
    if (dest == 1): # ACTION = 1
        # Move
        loc = move(client_socket, header)
    elif (dest == 2 and loc != stations[2]): # ACTION = 2
        # Pick up but not at the pantry
        client_socket.send(pickle.dumps([2]))
    elif (dest == 3): # ACTION = 3
        # Put down item
        client_socket.send(pickle.dumps([3]))
    elif (dest == 4 or (dest == 2 and loc == stations[2])): # Gesture/Speech
        # Pick up item if currently at the ingredients pantry
        if (loc == stations[2]): # ACTION = 4
            # Replace w/ relevant speech later!
            speech = input("Select an item from the pantry:\n") 
            client_socket.send(pickle.dumps([4, speech]))
        else: # ACTION = 4
            gesture = 1 # Replace w/ relevant gesture later!
            client_socket.send(pickle.dumps([4, gesture]))
    elif (dest == 5): # ACTION = 5
        # Attempt to submit our dish
        client_socket.send(pickle.dumps([5]))
    elif (dest == 6): # ACTION = 6
        # Throw away our inventory!
        client_socket.send(pickle.dumps([6]))
    elif (dest == 7): # ACTION = 7
        # Throw away everything at the station!
        client_socket.send(pickle.dumps([7]))
    elif (dest == 8): # ACTION = 8
        sys.exit()
    
    return loc

# Class: Station Manager
class Kitchen_Stations:
    # Constructor method to initialize all kitchen stations
    def __init__(self, stations, idx):
        # Store stations in list for versatility of access
        self.idx = idx # Index of where the ingredient stand is
        self.stations = stations
        self.stations_list = []
        
        for name in stations:
            self.stations_list.append(Station(name))
            pass
        
    # Determine if station is empty
    def is_empty(self, station_name):
        if (self.stations_list[self.stations.index(station_name)].ingredients == []):
            return True
        else:
            return False
    
    # Set down item onto the kitchen station
    def add_item(self, station_name, item):
        # Place our inventory onto a station
        self.stations_list[self.stations.index(station_name)].ingredients.append(item)
        
    # Find item if choosing at a station
    def find_item(self, station_name, target):
        # Loop through the station's ingredients to see if we found it
        for item in self.stations_list[self.stations.index(station_name)].ingredients:
            # N.B. We will only deal with ingredients, NOT PLATES FOR NOW
            if (item.ingredient_name == target): return item
        
        return None
        
    # Pick up item from the kitchen station
    def pick_item(self, station_name, target=None):
        # Do nothing if the station has no item
        if (self.stations_list[self.stations.index(station_name)].ingredients == []):
            return None
        
        # Pick up target item if specified
        if (target != None):
            item = self.find_item(station_name, target)
            
            # Remove item from the station, if valid
            if (item != None):
                self.stations_list[self.stations.index(station_name)].ingredients.remove(item)
            return item
        
        # Pick up item from station and clear the station (N.B. Fix for pantry)
        item = self.stations_list[self.stations.index(station_name)].ingredients[0]
        
        # Remove item from the station
        self.stations_list[self.stations.index(station_name)].ingredients.remove(item)
        
        # # N.B. If at plates cupboard/pantry, DO NOT clear the station
        # if (station_name != stations[2] and station_name != stations[3]):
        #     self.stations_list[self.stations.index(station_name)].ingredients.clear()
        return item
    
    # Set the old station to be denoted empty/free
    def set_free(self, station_name):
        self.stations_list[self.stations.index(station_name)].busy = False
    
    # Set the target station to be denoted busy
    def set_busy(self, station_name):
        self.stations_list[self.stations.index(station_name)].busy = True
        
    # Print out the states of every station in the kitchen
    def display_kitchen(self):
        status = ""
        for location in self.stations_list:
            message = location.station_name
            message += ", " + str(location.ingredients)
            message += ", busy: " + str(location.busy)
            message += " ||| "
            status += message
        print(status)
        
# Class: Station
class Station:
    # Constructor method to initialize a kitchen station
    def __init__(self, station_name):
        self.station_name = station_name
        self.ingredients = [] # Initialize station to have no ingredients
        self.busy = False # Initialize station to be free    

# Class: Player
class Player:
    # Constructor method to initialize game player
    def __init__(self, name):
        self.name = name
        
        # Initialize with empty inventories and beginning at the start location
        self.location = None # N.B. String of station name
        self.inventory = []
        
# Plate Class
class Plate:
    def __init__(self, ID_number):
        self.ID_number = ID_number # Identifier
        self.contents = []
        
    def plate_item(self, item):
        self.contents.append(item)
        
# Ingredient Class
class Ingredient:
    def __init__(self, name, cut_state, cook_state, process_station):
        self.ingredient_name = name
        self.cut_state = cut_state
        self.cook_state = cook_state
        self.process_station = process_station
        
    def compare(self, ingred2):
        # Compare two ingredients' by similarity
        cut = abs(self.cut_state - ingred2.cut_state)
        cook = abs(self.cook_state - ingred2.cook_state)
        return cut + cook
        
# Recipe Class
class Recipe:
    def __init__(self, materials):
        self.materials = materials
        
    # Return the string representation of the recipe
    def recipe_string(self):
        representation = ""
        mats = []
        
        for item in self.materials:
            raw = "["
            details = [str(item.ingredient_name), str(item.cut_state), 
                       str(item.cook_state), str(item.process_station)]
            raw += ", ".join(details) + "]"
            mats.append(raw)
        
        return mats
        
    # Attribute a score to the target recipe
    def score_dish(self, dish):
        # Dish is a plate with all the necessary ingredients
        target_dish = copy.deepcopy(self.materials)
        test_dish = copy.deepcopy(dish)
        
        score = 0
        
        # Evaluate each element of the dish
        for item in test_dish:
            match = [part for part in target_dish if part.ingredient_name == item.ingredient_name]
            
            # Calculate the score for each item
            if (match == []):
                # No match found, we added a wrong ingredient!
                score -= 5
            else:
                target_item = match[0]
                diff = target_item.compare(item)
                score -= diff * 1 # Every different in cut/cook is penalized
            
            # Remove the items from our copies!
            target_dish.remove(match[0])
            pass
        
        return score

     

    
