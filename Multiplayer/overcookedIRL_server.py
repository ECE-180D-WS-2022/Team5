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

# %% Game Configuration
stations = ["Cutting Board", "Stove", "Ingredients Stand", 
            "Plates Cupboard", "Submission Countertop", "Share Station"]
config = {"host": "131.179.50.229", "port": 4900, "stations": stations,
          "player_num": 2, "HEADER": 4096}

# %% Setup Socket Server
# Define server connection parameters
# host = "131.179.50.229" # IPv4 address of the Eng. IV lab room
# host = "192.168.1.91" # IPv4 address of my (K's) apartment
host = config["host"]
port = config["port"] # Unique 4 digit code to verify socket connections
server = socket.socket()

# Define operation runtime parameters
thread_count = 0 # Number of threaded processes connected to the server
HEADER = config["HEADER"] # Maximum number of bytes for data transmission, i.e. 4096 bytes

# %% Initialize Game Server
# Create our target recipe


# Connect game server online
try:
    server.bind((host, port))
    print("Server bound successfully!")
except socket.error as e:
    print("Our error message:", str(e))

# Define a max limit of 5 threaded client connections
server.listen(5)

# %% Define Thread Process
# Function: Controls thread process
def threaded_client(connection, player, player_ID, kitchen, target, config, kitchen1):
    # Continuously receive and process client data
    count = 0
    # player = None # N.B. At the start, player has not been created yet
    
    while True:
        count += 1
        
        data = pickle.loads(connection.recv(HEADER))
        player = process_data(connection, player, data, kitchen, target, kitchen1)
        
        # Print state of game for each while loop iteration
        print_state(count, data, player, player_ID)
        
        # Print game state for all stations
        kitchen.display_kitchen()
        
        # Send game state to player client after first iteration
        print("Sent game state:")
        game_state = get_status(count, stations, 
                                kitchen, player, target, player_ID)
        connection.send(pickle.dumps(game_state))
        print(game_state)
        
        print("##########################################")
        pass

# Function: Retrieve the entire game status
def get_status(count, stations, kitchen, player, target_recipe, player_ID):
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
        inventory += "Plate: " + ", ".join([item.ingredient_name for item in player.inventory[0].contents])
    inventory += "]"
    
    # Aggregate contents of the pantry
    pantry = "["
    pantry += ", ".join([item.ingredient_name for item in kitchen.stations_list[2].ingredients])
    pantry += "]"
    
    # Retrieve target recipe
    target = target_recipe.recipe_string()
    
    # Retrieve share station
    share = "["
    share_items = []
    
    for item in kitchen.stations_list[5].ingredients:
        if (type(item) == Ingredient):
            name = item.ingredient_name
            cut_state = item.cut_state
            cook_state = item.cook_state
            state = str(cut_state) + "-" + str(cook_state)
            share_items.append("Item: " + str(name) + " | State: " + str(state))
        else: # (type(item) == Plate):
            name = item.ID_number
            contents = [raw.ingredient_name for raw in item.contents]
            contents = "/".join(contents)
            share_items.append("Plate ID: " + str(name) + " | Contents: " + str(contents))
        pass
    
    share += "|||||".join(share_items)
    share += "]"
    
    return [loc, inventory, pantry, target, share]

# Function: Print out the status of the player
def print_state(count, data, player, player_ID):
    print("For iteration number:", str(count))
    print("Our connection received data:", str(data))
    print("Our current player:", str(player.name), ", w/ ID:", str(player_ID))
    print("Our inventory size:", str(len(player.inventory)))
    
    for item in player.inventory:
        if (type(item) == Ingredient):
            name = item.ingredient_name
            cut_state = item.cut_state
            cook_state = item.cook_state
            state = str(cut_state) + "-" + str(cook_state)
            print("Item:", str(name), "| State:", str(state))
        else: # (type(item) == Plate):
            name = item.ID_number
            contents = [raw.ingredient_name for raw in item.contents]
            contents = "/".join(contents)
            print("Plate ID:", str(name), "| Contents:", str(contents))

# Function: Processes client data to alter game state
def process_data(connection, player, data, kitchen, target, kitchen1):
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
                
                # If at the share station, also remove item from the other player
                if (player.location == stations[5]):
                    trash = kitchen1.pick_item(station_name)
                
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
                
                # Make item visible on both players if at share station
                if (player.location == stations[5]):
                    kitchen1.add_item(station_name, item)
                    
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
        
# Function: Game server-side initialization
def game_init(pantry_idx, config):
    # Set up all kitchen stations
    kitchens = [Kitchen_Stations(config["stations"], 
                                 pantry_idx) for i in range(config["player_num"])]
    
    # Choose a target recipe for each party
    targets = [generate_recipe() for i in range(config["player_num"])]
    
    # Add ingredients and plates to each kitchen
    for kitchen in kitchens:
        recipe = targets[kitchens.index(kitchen)]
        required_ingredients = set(recipe.get_ingredients())
        
        # Add necessary ingredients
        for item in required_ingredients:
            kitchen.add_item(stations[pantry_idx], Ingredient(item, 0, 0))
            pass
        
        # Add plates
        kitchen.add_item(stations[3], Plate(0))
        pass
    
    # Return a kitchen manager for each player, as they should have their own
    return kitchens, targets

# %% Run Game on Client-Side
clients = []
players = []
addresses = []
kitchens, targets = game_init(2, config)
config["kitchens"] = kitchens
config["targets"] = targets

while True:
    # Receive a client connection
    client, address = server.accept() 
    thread_count += 1 # Increase the number of threaded processes per client
    
    # Print our confirmation message of client connection
    print("Connected to:", str(address[0]), ":", str(address[1]),
          " ||||| ", "Number of threads:", str(thread_count))
    
    clients.append(client)
    addresses.append(address)
    players.append(Player(pickle.loads(client.recv(HEADER))[1]))
    
    # Wait for all players to at least establish connection before proceeding
    if (thread_count == config["player_num"]): 
        clients[0].send(pickle.dumps(True))
        clients[1].send(pickle.dumps(True))
        
        # Wait for ready signal from BOTH PLAYERS
        ready1 = pickle.loads(clients[0].recv(HEADER))
        ready2 = pickle.loads(clients[1].recv(HEADER))
        
        # Send confirmation for synchronized start
        clients[0].send(pickle.dumps(ready1))
        clients[1].send(pickle.dumps(ready2))
        
        # Begin game logic on the server side
        start_new_thread(threaded_client, (clients[0], players[0], 0, 
                                           kitchens[0], targets[0], config, kitchens[1]))
        start_new_thread(threaded_client, (clients[1], players[1], 1, 
                                           kitchens[1], targets[1], config, kitchens[0]))
    pass  

# %% Testing Cell
import numpy as np
class c1():
    def __init__(self, x, y):
        pass

class c2():
    def __init__(self, xy, xz, yz):
        self.xy = c1(0, 0)

tester = c2(1, 2, 3)
# %% Testing Cell 2
lll = []
lll.append(("hello" ,"world"))
print(lll)
