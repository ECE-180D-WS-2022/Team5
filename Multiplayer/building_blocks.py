# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:43:02 2022

@author: Kellen Cheng
"""

# Import Statements
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
    4    -> Perform Gesture/Speech
    
'''
###############################################################################


def process_action(kitchen, player, data, connection):
    # kitchen -> station manager
    
    # Figure out action type
    if (data[0] == 1): # We know the player is moving to another station
        # Worry about error handling for moving to an already busy station LATER
        if (player.location != "Starting Position"):
            current_station = kitchen.stations.index(player.location)
            kitchen.stations[current_station].busy = 0 # Set it to not be busy!
        player.location = kitchen.stations[data[1] - 1].station_ID
        kitchen.stations[data[1] - 1].busy = 1 # Set it to be busy!
        pass
    elif (data[0] == 2): # We know the player wants to pick up item
        pass
    elif (data[0] == 3): # We want to put down item
        if (player.inventory != [] and player.inventory[0].process_station == player.location.station_ID):
            raw = player.inventory[0] # Retrieve ingredient
            kitchen.stations[kitchen.stations.index(player.location)].ingredient.append(raw)
            pass
        pass
    elif (data[0] == 4): # We want to perform a gesture/pick up ingredient
        if (player.location == kitchen.stations[2].station_ID and player.inventory == []): # AKA ingredients station
            print("---IN HERE---")
            connection.send(pickle.dumps([True]))
            selection = pickle.loads(connection.recv(HEADER))
            
            data = selection
            
            selection = Ingredient(selection, 0, "Cutting Station")
            player.inventory.append(selection)
        elif (player.location == kitchen.stations[2].station_ID and player.inventory != []):
            print("---Should be in here??---")
            connection.send(pickle.dumps([False]))
            pass
        pass
    
    return data
    pass

def game_start(client_socket, header=HEADER):
    print("Please select one of the following options:")
    choice = int(input("(1) New Save (2) Load Save (3) Exit: "))
    
    if (choice == 3): pass
    elif (choice == 2): return("Testing")
    else: 
        register(client_socket, header)

def move(client_socket, header=HEADER): # ACTION=1
    print("Please choose a station from one of the options below: ")
    choice = int(input("(1) Chopping Board (2) Stove (3) Ingredients (4) Submit (5) Share (6) Plate "))
    while (choice not in [1,2,3,4,5,6]):
        choice = int(input("Please select a valid station: "))
    
    # client_socket.send(str.encode(str(choice)))
    client_socket.send(pickle.dumps([1, choice]))
    
    station_name = None
    if (choice == 3): station_name = "Ingredients Station"
    
    action(client_socket, header, station_name)
    
# def action(client_socket, header=HEADER, current_station="Game Start"):
#     print("You are currently at the " + current_station)
#     next_move = int(input("(1) Move (2) Pick up (3) Put down (4) Action/Gesture (5) Submit"))
    
#     while (next_move not in [1,2,3,4,5]):
#         next_move = int(input("Please reselect a valid option: "))
    
#     if (next_move == 1): # ACTION = 1
#         move(client_socket, header)
#     elif (next_move == 2): # ACTION = 2
#         # client_socket.send(pickle.dumps[2, None])
#         pass # Do something
#     elif (next_move == 3): # ACTION = 3
#         client_socket.send(pickle.dumps([3]))
        
#         action(client_socket, header, current_station)
#         pass # Do something
#     elif (next_move == 4): # ACTION = 4
#         ingredient_or_gesture = 0 # Placeholder for now!
#         client_socket.send(pickle.dumps([4, ingredient_or_gesture]))
#         server_response = pickle.loads(client_socket.recv(header))
        
#         print("Our server response is: ", str(server_response))
        
#         if (server_response[0] == True): # Confirm we at ingredients stand and move valid
#             selection = input("Choose an ingredient from [fish, beans, chili peppers]: ")
#             client_socket.send(pickle.dumps(selection))
#             print("Here1")
#         else:
#             print("Here2")
#             print("Your inventory is full!")
        
#         action(client_socket, header, current_station)
#         pass # Do something
#     elif (next_move == 5):
#         pass # Do something
    
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
    
    # Begin game logic
    while True:
        current = action(client_socket, header=HEADER, loc=current)
   
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
    print("_________________________________________________")
    print("Select an option from one of the following below:")
    dest = int(input("(1) Move (2) Pick Up (3) Put Down" \
                 " (4) Gesture/Speech (5) Submit\n"))
    
    if (dest == 1): # Move
        loc = move(client_socket, header)
    elif (dest == 2 and loc != stations[2]): # Pick up but not at the pantry
        client_socket.send(pickle.dumps([2]))
    elif (dest == 3): # Put down
        client_socket.send(pickle.dumps([3]))
    elif (dest == 4 or (dest == 2 and loc == stations[2])): # Gesture/Speech
        # Pick up item if currently at the ingredients pantry
        if (loc == stations[2]): # ACTION = 4
            speech = "Lettuce" # Replace w/ relevant speech later!
            client_socket.send(pickle.dumps([4, speech]))
        else: # ACTION = 4
            gesture = 1 # Replace w/ relevant gesture later!
            client_socket.send(pickle.dumps([4, gesture]))
    
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
        
    # Pick up item from the kitchen station
    def pick_item(self, station_name):
        # Do nothing if the station has no item
        if (self.stations_list[self.stations.index(station_name)].ingredients == []):
            return None
        
        # Pick up item from station and clear the station (N.B. Fix for pantry)
        item = self.stations_list[self.stations.index(station_name)].ingredients[0]
        self.stations_list[self.stations.index(station_name)].ingredients.clear()
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
    def __init__(self, ID_number, empty):
        self.ID_number = ID_number # Identifier
        self.empty = empty # True -> empty, False -> plate filled
        self.ingredients = []
        
# Ingredient Class
class Ingredient:
    def __init__(self, name, state, process_station):
        self.ingredient_name = name
        self.state = state
        self.process_station = process_station
     

    
