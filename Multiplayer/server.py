# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:39:00 2022

@author: Kellen Cheng
"""

# Import Statements
import sys
import time
import pickle
import socket
import threading
from _thread import *
from building_blocks import *

# %% Server Configuration
config = dict()
config["Host"] = "FILL WITH OWN IPV4 ADDRESS" # IPv4 address of ENG IV lab room
config["Port"] = 4900 # Unique ID, can be any number but must match client's
config["HEADER"] = 4096 # Defines max number of byte transmission
config["Player_Num"] = 4 # Configure the number of players for the server
config["Thread_Count"] = 0 # Stores the number of threaded processes running

# %% Server Setup
# Create the server socket
server = socket.socket()

# Connect the server online
try:
    server.bind((config["Host"], config["Port"]))
    print("STATUS -> Server bound successfully!")
except socket.error as e:
    print("ERROR ->", str(e))
    
# Limit the server to 5 connections (with one connection as leeway in case)
server.listen(config["Player_Num"] + 1)

# Remove blocking synchronous servers in favor of realtime nonblocking logic
server.setblocking(False)

# %% Server Methods
# Function : Threading function that checks for data updates in the background
def update_state(clients):
    prev_state = [None, None]
    
    # In threaded background, continuously check for a change in game state
    while (True):
        current_state = copy.deepcopy(temporary_data)
        if (current_state != prev_state):
            # Send the updated data to the players
            for client in clients:
                client.send(pickle.dumps(current_state))
            prev_state = current_state
            
        # Set delay to avoid retrieving state between internal actions
        time.sleep(0.10)
        pass
    pass

# Function : threaded function to take care of each client's actions
def threaded_client(clients, ID, temp_game_data):
    # Set a dedicated thread for checking for updates to the game state
    input_thread = threading.Thread(target=update_state, 
                                    args=(clients, ), 
                                    daemon=True)
    input_thread.start()
    
    # Check for game data
    while True:
        data = get_unblocked_data(clients[ID])
        if data == None: continue
        temp_game_data[ID] = data
        
        print("Server data from client:", str(ID), ",", str(data),
              "||", str(temporary_data[0]), ",", str(temporary_data[1]))
        
    pass

# %% Control Loop
clients = []
temporary_data = [None, None]

while True:
    # Listen for client connections
    client, address = get_accept(server)
    
    # Update the count of threaded processes
    config["Thread_Count"] += 1
    
    # Print confirmation addresses of the connection
    print("Connected to", str(address[0]), ":", str(address[1]))
    
    # Store each connection
    clients.append(client)
    
    # Begin new threaded process for each player
    if (len(clients) == 2):
        # Send the true condition
        clients[0].send(pickle.dumps(True))
        clients[1].send(pickle.dumps(True))
        
        start_new_thread(threaded_client, (clients, 0, temporary_data))
        start_new_thread(threaded_client, (clients, 1, temporary_data))
    pass



















