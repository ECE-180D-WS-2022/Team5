# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:43:02 2022

@author: Kellen Cheng
"""

# Import Statements
import os
import sys
import time
import socket
import pickle
import numpy as np
HEADER = 4096

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
    elif (data[0] == 4): # We want to perform a gesture/pick up ingredient
        if (player.location == kitchen.stations[2] and player.inventory == []): # AKA ingredients station
            ingredient = connection.send(pickle.dumps([True]))
            selection = pickle.loads(connection.recv(HEADER))
            player.inventory.append(selection)
        pass
    pass

def game_start(client_socket, header=HEADER):
    print("Please select one of the following options:")
    choice = int(input("(1) New Save (2) Load Save (3) Exit: "))
    
    if (choice == 3): sys.exit()
    elif (choice == 2): return("Testing")
    else: 
        register(client_socket, header)

def register(client_socket, header=HEADER):
    name = input("Please enter your player name: ")
    # client_socket.send(str.encode(name))
    client_socket.send(pickle.dumps(name))
    # confirmation = client_socket.recv(header)
    # recipe = client_socket.recv(header)
    confirmation = pickle.loads(client_socket.recv(header))
    recipe = pickle.loads(client_socket.recv(header))
    print(confirmation)
    print(recipe)
    move(client_socket, header)
    
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
    
def action(client_socket, header=HEADER, current_station="Game Start"):
    print("You are currently at the " + current_station)
    next_move = int(input("(1) Move (2) Pick up (3) Put down (4) Action/Gesture (5) Submit"))
    
    while (next_move not in [1,2,3,4,5]):
        next_move = int(input("Please reselect a valid option: "))
    
    if (next_move == 1): # ACTION = 1
        move(client_socket, header)
    elif (next_move == 2): # ACTION = 2
        # client_socket.send(pickle.dumps[2, None])
        pass # Do something
    elif (next_move == 3):
        pass # Do something
    elif (next_move == 4): # ACTION = 4
        ingredient_or_gesture = 0 # Placeholder for now!
        client_socket.send(pickle.dumps([4, ingredient_or_gesture]))
        server_response = pickle.loads(client_socket.recv(header))
        
        if (server_response[0] == True): # Confirm we at ingredients stand and move valid
            selection = input("Choose an ingredient from [fish, beans, chili peppers]: ")
            client_socket.send(pickle.dumps(selection))
        
        action(client_socket, header, current_station)
        pass # Do something
    elif (next_move == 5):
        pass # Do something
    
    
# Station Manager Class
class Station_Manager:
    def __init__(self):
        self.stations = []

        S1 = Station("Cutting Station", None)
        self.stations.append(S1)

        S2 = Station("Stove Station", None)
        self.stations.append(S2)

        S3 = Station("Ingredients Station", None)
        self.stations.append(S3)

        S4 = Station("Submit Station", None)
        self.stations.append(S4)

        S5 = Station("Share Station", None)
        self.stations.append(S5)

        S6 = Station("Plate Station", None)
        self.stations.append(S6)

# Station Class
class Station:
    def __init__(self, station_ID, ingredient):
        self.station_ID = station_ID
        # self.location = self.station_name
        self.ingredient = [] #current ingredient at the station
        self.busy = 0 # 0 is not busy, so able to place item here; 1 means busy, so cannot place item here

# Player Class
class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.location = "Starting Position"
        self.plate = []
        
# Plate Class
class Plate:
    def __init__(self, ID_number, empty):
        self.ID_number = ID_number # Identifier
        self.empty = empty # True -> empty, False -> plate filled
        self.ingredients = []
     

    
