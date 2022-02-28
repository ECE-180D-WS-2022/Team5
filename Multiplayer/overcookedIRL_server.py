# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 17:38:13 2022

@author: Kellen Cheng
"""

# Import Statements
import sys
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
host = "131.179.51.6" # IPv4 address of the Eng. IV lab room
host = "192.168.1.91" # IPv4 address of my (K's) apartment
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

# Add ingredients
kitchen.add_item(stations[2], Ingredient("Lettuce", 0, stations[0]))

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
        print("##########################################")
        pass

# Function: Print out the status of the player
def print_state(count, data, player):
    print("For iteration number:", str(count))
    print("Our connection received data:", str(data))
    print("Our current player:", str(player.name))
    print("Our inventory size:", str(len(player.inventory)))
    
    for item in player.inventory:
        name = item.ingredient_name
        state = item.state
        process_station = item.process_station
        print("Item:", str(name), "| State:", str(state), \
              " | Process Station:", str(process_station))
        pass

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
            else: # player.inventory != []
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
            player.inventory.clear()
            kitchen.add_item(station_name, item)
        else: # player.inventory == []
            print("Nothing to put down!")
    elif (data[0] == 4): # Action code 4
        # Pick up ingredient if at the pantry
        if (player.location == stations[2]):
            # Pick up item only if inventory is empty and pantry stocked!
            if (player.inventory == [] and (not kitchen.is_empty(player.location))):
                item = kitchen.pick_item(stations[2]) # Retrieve ingredient
                player.inventory.append(item) # Add to our inventory
            else: # player.inventory != [] or kitchen.is_empty(player.location)
                print("Inventory full or station empty! Cannot pick up item!")
        else: # Process the ingredient if we are at the correct station!
            # Double check that the ingredient is present first!
            if (not kitchen.is_empty(player.location)):
                # Ensure we are at the correct station to process ingredient!
                if (kitchen.stations_list[stations.index(player.location)].ingredients[0].process_station == player.location):
                    kitchen.stations_list[stations.index(player.location)].ingredients[0].state += 1
                else:
                    print("Incorrect station to process!")
            else:
                print("No ingredient to process!")
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


