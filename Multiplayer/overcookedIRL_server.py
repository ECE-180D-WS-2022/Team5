# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 17:38:13 2022

@author: Kellen Cheng
"""

# Import Statements
import sys
import time
import pickle
import socket
from _thread import *
from building_blocks import *

'''
N.B. Refer to the below link for the base theory behind the code:
    https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/
'''

# %% Setup Socket Server
# Define server connection parameters
host = "131.179.51.146" # IPv4 address of the Eng. IV lab room
# host = "192.168.1.91" # IPv4 address of my (K's) apartment
port = 4900 # Unique 4 digit code to verify socket connections
server = socket.socket()

# Define operation runtime parameters
thread_count = 0 # Number of threaded processes connected to the server
HEADER = 4096 # Maximum number of bytes for data transmission, i.e. 4096 bytes

# %% Initialize Game Server
# Setup kitchen stations
stations = ["Cutting Board", "Stove", "Ingredients Stand", 
            "Plates Cupboard", "Submission Countertop", "Share Station"]
kitchen = Kitchen_Stations(stations, 2) # Int is index of ingredients stand

# Add ingredients to the pantry
kitchen.add_item(stations[2], Ingredient("Lettuce", 0, 0, [stations[0], stations[1]]))
kitchen.add_item(stations[2], Ingredient("Beef", 0, 0, [stations[0], stations[1]]))

# Add plates to the plate cupboard
kitchen.add_item(stations[3], Plate(0))
kitchen.add_item(stations[3], Plate(1))

# Create our target recipe
target = Recipe([Ingredient("Lettuce", 1, 1, [stations[0], stations[1]]),
                 Ingredient("Beef", 2, 2, [stations[0], stations[1]])])

# Connect game server online
try:
    server.bind((host, port))
    print("Server bound successfully!")
except socket.error as e:
    print("Our error message:", str(e))

# Define a max limit of 5 threaded client connections
server.listen(5)

'''
Get rid of prepare stations, implement kitchen manager set up, revamp Recipe
class to be filled with recipes. Have pantry have unlimited options.
'''

# %% Define Thread Process
# Function: Controls thread process
def threaded_client(connection):
    # Continuously receive and process client data
    count = 0
    player = None # N.B. At the start, player has not been created yet
    
    while True:
        count += 1
        
        data = pickle.loads(connection.recv(HEADER))
        player = process_data(connection, player, data)
        
        # Print state of game for each while loop iteration
        print_state(count, data, player)
        
        # Print game state for all stations
        kitchen.display_kitchen()
        
        # Send game state to player client after first iteration
        if (count != 1): 
            print("Sent game state:")
            game_state = get_status(count, stations, kitchen, player, target)
            connection.send(pickle.dumps(game_state))
            print(game_state)
        
        print("##########################################")
        pass

# Function: Retrieve the entire game status
def get_status(count, stations, kitchen, player, target_recipe):
    '''
    Returns [player location, current inventory, pantry, target recipe]
    '''
    # Retrieve location
    loc = player.location
    
    # Aggregate contents of the inventory
    inventory = "["
    
    if (player.inventory != [] and type(player.inventory[0]) == Ingredient):
        inventory += ", ".join([item.ingredient_name for item in player.inventory])
    elif (player.inventory != [] and type(player.inventory[0]) == Plate):
        inventory += ", ".join([item.ingredient_name for item in player.inventory[0].contents])
    inventory += "]"
    
    # Aggregate contents of the pantry
    pantry = "["
    pantry += ", ".join([item.ingredient_name for item in kitchen.stations_list[2].ingredients])
    pantry += "]"
    
    # Retrieve target recipe
    target = target_recipe.recipe_string()
    
    return [loc, inventory, pantry, target]

# Function: Print out the status of the player
def print_state(count, data, player):
    print("For iteration number:", str(count))
    print("Our connection received data:", str(data))
    print("Our current player:", str(player.name))
    print("Our inventory size:", str(len(player.inventory)))
    
    for item in player.inventory:
        if (type(item) == Ingredient):
            name = item.ingredient_name
            cut_state = item.cut_state
            cook_state = item.cook_state
            state = str(cut_state) + "-" + str(cook_state)
            process_station = item.process_station
            print("Item:", str(name), "| State:", str(state), \
                  " | Process Station:", str(process_station))
        else: # (type(item) == Plate):
            name = item.ID_number
            contents = [raw.ingredient_name for raw in item.contents]
            contents = "/".join(contents)
            print("Plate ID:", str(name), "| Contents:", str(contents))

# Function: Processes client data to alter game state
def process_data(connection, player, data):
    # Receive data as list, where data[0] defines the type of action performed
    if (data[0] == 0 and player == None): # Action code 0
        # Game would like to register new player
        print("Server has received instruction to initialize new player with" \
              " name as follows:", str(data[1]))
        player = Player(data[1])
    elif (data[0] == 1): # Action code 1
        # Game would like to move the player to a different station
        dest = data[1] - 1 # Index of new destination station
        dest_name = stations[dest] # Turn index into the station name
        old_station = player.location # N.B. Already a station name!
        
        # Reset old station to be free, unless at the start
        if (old_station != None):
            kitchen.set_free(old_station)
        
        # Set new station to be busy
        kitchen.set_busy(dest_name)
        
        # Update player location
        player.location = dest_name
    elif (data[0] == 2): # Action code 2
        # Pick up ingredient if NOT AT the pantry
        if (player.location != stations[2]):
            if (player.inventory == []):
                station_name = player.location
                item = kitchen.pick_item(station_name)
                
                # If item is None, station had no item to begin with
                if (item != None): player.inventory.append(item)
                else: print("Station empty! No item to pick up!")
            elif (type(player.inventory[0]) == Plate):
                # Pick up item and put it onto our plate!
                station_name = player.location
                item = kitchen.pick_item(station_name)
                
                # If item is Non, station had no item to begin with
                if (item != None):
                    player.inventory[0].plate_item(item)
                else:
                    print("Station empty! No item to put on the plate!")
                pass
            else: # player.inventory != [] and type(player.inventory[0]) != Plate
                print("Inventory full! Cannot pick up item!")
            pass
        else: # N.B. Should be a double check
            print("Still under development...")
    elif (data[0] == 3): # Action code 3
        # Put down item, if we have any item to put down
        station_name = player.location
        
        if (player.inventory != []):
            # Fetch our item, then clear our inventory
            item = player.inventory[0]
            
            if (type(item) == Ingredient and 
                (station_name == stations[3] or station_name == stations[4])):
                # Can't place ingredients at the plate or submit stations!
                print("Can't put down ingredients at the", str(station_name))
            elif (type(item) == Plate and station_name == stations[2]):
                # Can't put down plate at the ingredients stand
                print("Can't put down a plate at the ingredients stand!")
            elif (not kitchen.is_empty(player.location) and
                  (station_name != stations[2] and station_name != stations[3])):
                # Can't put down item at an occupied station!
                print("Can't put down item at an occupied station!")
            else:
                player.inventory.clear()
                kitchen.add_item(station_name, item)
        else: # player.inventory == []
            print("Nothing to put down!")
    elif (data[0] == 4): # Action code 4
        # Pick up ingredient if at the pantry
        if (player.location == stations[2]):
            # Pick up item only if inventory is empty and pantry stocked!
            if (player.inventory == [] and (not kitchen.is_empty(player.location))):
                item = kitchen.pick_item(stations[2], data[1]) # Retrieve ingredient
                
                # If the request was for nonexistent ingredient, do nothing
                if (item == None):
                    print("You asked for an invalid ingredient!")
                else:
                    player.inventory.append(item) # Add to our inventory
            else: # player.inventory != [] or kitchen.is_empty(player.location)
                print("Inventory full or station empty! Cannot pick up item!")
        else: # Process the ingredient if we are at the correct station!
            # Double check that the ingredient is present and station is valid
            if (player.location != stations[0] and player.location != stations[1]):
                print("We aren't at a valid processing station!")
            elif (not kitchen.is_empty(player.location)):
                # Ensure we are at the correct station to process ingredient!
                if (player.location in kitchen.stations_list[stations.index(player.location)].ingredients[0].process_station):
                    # Depending on if we are at the stove/cutting board, modify
                    if (player.location == stations[0]): # Cutting board
                        kitchen.stations_list[stations.index(player.location)].ingredients[0].cut_state += 1
                    elif (player.location == stations[1]): # Stove
                        kitchen.stations_list[stations.index(player.location)].ingredients[0].cook_state += 1
                else:
                    print("Incorrect station to process!")
            else:
                print("No ingredient to process!")
    elif (data[0] == 5): # Action code 5
        # Submit our materials to the chef!
        if (player.location == stations[4] and not kitchen.is_empty(player.location)):
            # Ensure we are submitting a plated final dish
            if (type(kitchen.stations_list[stations.index(player.location)].ingredients[0]) == Plate):
                score = target.score_dish(kitchen.stations_list[stations.index(player.location)].ingredients[0].contents)
                print("Your dish received the score:", str(score))
            else:
                print("How can you serve unplated food to the chef??")
            pass
        else:
            print("We aren't at the dish submission station or it's empty!")
        pass
    elif (data[0] == 6): # Action code 6
        # Trash our current inventory
        player.inventory = []
    elif (data[0] == 7): # Action code 7
        # Trash our current station, excluding the plate and pantry stations!
        if (player.location != stations[2] and player.location != stations[3]):
            kitchen.stations_list[stations.index(player.location)].ingredients = []
        else:
            print("We can't throw all stuff at this station!")
    else:
        print("Still under development...")
        
    # Return the new player state after any alterations
    return player
        
# %% Run Game on Client-Side
while True:
    client, address = server.accept() # Receive a client connection
    thread_count += 1 # Increase the number of threaded processes per client
    
    # Print our confirmation message of client connection
    print("Connected to:", str(address[0]), ":", str(address[1]),
          " ||||| ", "Number of threads:", str(thread_count))
    
    # Create a new thread process for our client
    start_new_thread(threaded_client, (client, ))
    pass

# %% Testing Cell

