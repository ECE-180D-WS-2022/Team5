# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 15:29:18 2022

@author: Kellen Cheng
"""


# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:43:02 2022

@author: Kellen Cheng
"""

# Import Statements
import os
import sys
import copy
import time
import queue
import socket
import pickle
import threading
import numpy as np

# # File Import Statements
# from config import *
# from player import *
# from sprites import *
# from counters import *
# from color_mouse import *
# from ingredients import * 

# %% Utility Functions

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

# Function: Prints the game status as an easy to read string
def print_status_as_string(status):
    # If dealing with a nonetype, print NONE and return
    if (status == None): 
        print("State is NONE!")
        return
    
    loc = status[0]
    inventory = status[1]
    pantry = status[2]
    target = status[3]
    share = status[4]
    ID = status[5]
    name = status[6]
    
    print("Current Player location:", loc)
    print("Current Player Inventory:", inventory)
    print("Pantry Ingredients:", pantry)
    print("Target Recipe:", target)
    print("Share Station:", share)
    print("Player ID:", str(ID), ", with Player Name:", name)

# Function: Get data (blocking version)
def get_data(client_socket, condition=None, count=0):
    # If we don't set a certain amount of timed data retrieval
    if (count == 0):
        while True:
            try: condition = pickle.loads(client_socket.recv(HEADER))
            except: condition = None
            
            if (condition != None): break
    else:
        while count > 0:
            try: condition = pickle.loads(client_socket.recv(HEADER))
            except: condition = None
            
            if (condition != None): break    
            count -= 1
    return condition

# Function: Get data (nonblocking version)
def get_unblocked_data(client_socket, condition=None):
    try: 
        condition = pickle.loads(client_socket.recv(HEADER))
        # print(condition)
        #print('in a pickle!!!')
    except: condition = None
    return condition

# Function: Blocked accept (blocking version)
def get_accept(server):
    while True:
        try: 
            client, address = server.accept() 
            break
        except: 
            pass
    return client, address

def game(client_socket):
    print("############### Welcome to Overcooked IRL ###############")
    current = None # Local copy of the name of the current player location
    
    # Set a dedicated thread for checking for updates to the game state
    input_thread = threading.Thread(target=retrieve_state, 
                                    args=(client_socket, ), 
                                    daemon=True)
    input_thread.start()
        
    # Begin game logic
    changes = 0
    while True:      
        # Move to a station on the first iteration, perform action otherwise
        if (changes == 0):
            current = move(client_socket, header=HEADER)
            changes = 1
        else:
            current = action(client_socket, header=HEADER, loc=current)
        print("_________________________________________________")

        # Prevent simultaneous erroneous fetching inbetween internal actions            
        time.sleep(0.01)
        pass
   
# Function: Register a game player
def register(client_socket, header=HEADER): # ACTION = 0
    name = input("Please enter your player's name:\n")
    client_socket.send(pickle.dumps([0, name])) # Send information to be stored
    
# Function: Move stations as a player
def move(client_socket, header=HEADER): # ACTION = 1
    print("Select a station from one of the following below:")
    print("(1) Cutting Board (2) Stove (3) Ingredients Stand" \
                 " (4) Plates Cupboard (5) Submission Countertop" \
                     " (6) Share Station\n")
    dest = int(input())
    client_socket.send(pickle.dumps([1, dest])) # Send information to be stored
    return stations[dest - 1]

# Function: Non-blocking input
def retrieve_state(client_socket):
    prev = None
    while (True):
        command = get_unblocked_data(client_socket)
        if (command != None and command != prev):
            prev = command
            # print(command)
            print_status_as_string(command)
            print("End of state:-----------------------")
        pass

# Function: Complete an action
def action(client_socket, header=HEADER, loc=None): # ACTION = VARIABLE
    print("Select an option from one of the following below:")
    print("(1) Move (2) Pick Up (3) Put Down" \
                 " (4) Gesture/Speech (5) Submit (6) Trash Inventory"\
                     " (7) Trash Station (8) Exit \n")
    dest = int(input())
    
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
