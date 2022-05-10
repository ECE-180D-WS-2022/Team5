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
from playground_building_blocks import *

# %% Server Configuration
config = dict()
# config["Host"] = "192.168.1.91" # IPv4 address of ENG IV lab room
config["Host"] = "192.168.1.91"
config["Host"] = "192.168.56.1"
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
def update_state(clients, startTime):
    prev_state = [None, None]
    
    # In threaded background, continuously check for a change in game state
    while (True):
        current_state = copy.deepcopy(temporary_data)
        
        # if (current_state == [None, None]): continue

        # if (prev_state == [None, None]):
        #     for client in clients:
        #         client.send(pickle.dumps([current_state, time.time() - startTime]))
        #     prev_state = current_state
        # elif (current_state[0][4] != prev_state[0][4] or 
        #       current_state[0][5] != prev_state[0][5]):
        #     for client in clients:
        #         client.send(pickle.dumps([current_state, time.time() - startTime]))
        #     prev_state = current_state
        
        # for client in clients:
        #     client.send(pickle.dumps([current_state, time.time() - startTime]))
        
        # if (current_state != None and 
        #     (prev_state != [None, None] and current_state[0][0] != prev_state[0][0] and
        #      current_state[0][1] != prev_state[0][1])):
        #     # Send the updated data to the players
        #     for client in clients:
        #         client.send(pickle.dumps(current_state))
        #     prev_state = current_state
        # elif (prev_state == [None, None] and current_state != None):
        #     for client in clients:
        #         client.send(pickle.dumps(current_state))
        #     prev_state = current_state
        # if (current_state != prev_state):
            # for client in clients:
            #     client.send(pickle.dumps(current_state))
            # prev_state = current_state

            
        # Set delay to avoid retrieving state between internal actions
        time.sleep(0.10)
        pass
    pass

# Function : threaded function to take care of each client's actions
def threaded_client(clients, ID, temp_game_data, startTime):
    # Set a dedicated thread for checking for updates to the game state
    input_thread = threading.Thread(target=update_state, 
                                    args=(clients, startTime, ), 
                                    daemon=True)
    input_thread.start()
    
    # Check for game data
    prev_Time = 0
    while True:
        data = get_unblocked_data(clients[ID])
        if data == None: 
            # print('data is none')
            if (round((time.time() - startTime), 2) > prev_Time + 1):
                prev_Time += 1
                clients[ID].send(pickle.dumps(round((time.time() - startTime), 2)))
            continue
        else:
            if (type(data) == list and data[0] == 99):
                clients[not ID].send(pickle.dumps(data))
                print(data)
        temp_game_data[ID] = data
        # loc = [data[0], data[1], data[2], data[3], data[4], data[5]]
        
        
        
        
        
        # print("Server data from client:", str(ID), ",", str(data),
        #       "||", str(temporary_data[0]), ",", str(temporary_data[1]))
        
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

        clients[0].send(pickle.dumps("ClientID: 0"))
        clients[1].send(pickle.dumps("ClientID: 1"))
        
        start_time = time.time()
        
        start_new_thread(threaded_client, (clients, 0, temporary_data, start_time))
        start_new_thread(threaded_client, (clients, 1, temporary_data, start_time))
    pass

