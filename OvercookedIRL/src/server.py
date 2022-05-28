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
import datetime
import threading
from _thread import *
from playground_building_blocks import *

# %% Server Configuration
config = dict()
config["Host"] = socket.gethostbyname(socket.gethostname()) # automatically get ip address
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
server.listen(3)

# Remove blocking synchronous servers in favor of realtime nonblocking logic
# server.setblocking(False)

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
    interval = datetime.timedelta(minutes=10.0)
    while True:
        data = get_unblocked_data(clients[ID])
        if data == None: 
            tick = time.perf_counter()
            print(type(tick))
            print(type(startTime))
            print(type(interval))
            time_left = interval - datetime.timedelta(seconds=tick-startTime)
            clients[ID].send(pickle.dumps([77, format_timedelta(time_left)]))
            
            
            # if (round((time.time() - startTime), 2) > prev_Time + 1):
            #     prev_Time += 1
            #     clients[ID].send(pickle.dumps(round((time.time() - startTime), 2)))
            continue
        elif (type(data) == list and len(data) != 0 and data[0] == 99):
            clients[not ID].send(pickle.dumps(data))
            print(data)
        elif (type(data) == list and len(data) != 0 and data[0] == 88):
            # Code for updating scores!
            game_scores[ID] = data[1]
            
            # Send the score to all other players
            clients[not ID].send(pickle.dumps(game_scores))
            pass
        temp_game_data[ID] = data
        # loc = [data[0], data[1], data[2], data[3], data[4], data[5]]
        
        
        
        
        
        # print("Server data from client:", str(ID), ",", str(data),
        #       "||", str(temporary_data[0]), ",", str(temporary_data[1]))
        
    pass

# %% Control Loop
clients = []
player_names = []
temporary_data = [None, None]
game_scores = [0, 0]
while True:
    # Listen for client connections
    client, address = get_accept(server)
    
    # Update the count of threaded processes
    config["Thread_Count"] += 1
    
    # Print confirmation addresses of the connection
    print("Connected to", str(address[0]), ":", str(address[1]))
    
    # Store each connection
    clients.append(client)
    # player_names.append(pickle.loads(client.recv(HEADER))[1])
    
    # Begin new threaded process for each player
    if (config["Thread_Count"] == 2):
        # Send the true condition
        clients[0].send(pickle.dumps(True))
        clients[1].send(pickle.dumps(True))
        
        # Wait for ready signal from BOTH PLAYERS
        ready1 = get_data(clients[0])
        ready2 = get_data(clients[1])
        
        #ready1 = pickle.loads(clients[0].recv(config["HEADER"]))
        #ready2 = pickle.loads(clients[1].recv(config["HEADER"]))

        # server.setblocking(False)
        time.sleep(1)
        # Send confirmation for synchronized start
        time.sleep(1)
        clients[0].send(pickle.dumps(ready1))
        clients[1].send(pickle.dumps(ready2))

        clients[0].send(pickle.dumps("ClientID: 0"))
        clients[1].send(pickle.dumps("ClientID: 1"))

        print('sent both')
        
        start_time = time.perf_counter()
        
        start_new_thread(threaded_client, (clients, 0, temporary_data, start_time))
        start_new_thread(threaded_client, (clients, 1, temporary_data, start_time))
    pass

