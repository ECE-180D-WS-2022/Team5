# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:39:00 2022
@author: Kellen Cheng
"""

# Import Statements
import sys
import math
import time
import pickle
import socket
import datetime
import threading
from _thread import *
from playground_building_blocks import *
import random

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

# Function : threaded function to take care of each client's actions
def threaded_client(clients, ID, temp_game_data, startTime):
    # Set a dedicated thread for checking for updates to the game state

    # Check for game data
    prev_Time = datetime.timedelta(seconds=10*60)
    interval = datetime.timedelta(minutes=10.0)
    server.setblocking(False)
    clients[ID].setblocking(False)
    prev_total_time = -1
    # count = -10

    while True:
        # count += 0
        data = get_unblocked_data(clients[ID])
        # print(data)

        if (type(data) == list and len(data) != 0 and data[0] == 99):
            # Sending item to the other player!
            print("Sending data1")
            print("Received:", str(data))
            clients[not ID].send(pickle.dumps(data))
            print("ID:", str(ID), "and not ID:", str(not ID))
            print("Client0:", str(clients[0]), ", Client1:", str(clients[1]))
        elif (type(data) == list and len(data) != 0 and data[0] == 88):
            # We need to update scores!
            # Code for updating scores!
            game_scores[ID] = data[1]
            
            # Send the score to all other players
            clients[not ID].send(pickle.dumps(data))
            pass
        else: 
            tick = time.perf_counter()
            time_left = interval - datetime.timedelta(seconds=tick-startTime)
            
            # if (ID==1):
            #     print(datetime.timedelta(seconds=math.ceil(time_left.total_seconds())))
            #     print(prev_Time)
            
            
            if (datetime.timedelta(seconds=math.ceil(time_left.total_seconds())) < prev_Time):
                clients[ID].send(pickle.dumps([77, format_timedelta(time_left)]))
                prev_Time = datetime.timedelta(seconds=math.ceil(time_left.total_seconds()))
            if(data != None):
                clients[not ID].send(pickle.dumps(data))
            # if (round((time.time() - startTime), 2) > prev_Time + 1):
            #     prev_Time += 1
            #     clients[ID].send(pickle.dumps(round((time.time() - startTime), 2)))
            
        temp_game_data[ID] = data
        # loc = [data[0], data[1], data[2], data[3], data[4], data[5]]
        
        # if(ID == 0):
        #     # print(time_left.total_seconds())
        #     t = math.ceil(time_left.total_seconds())
        #     print(t)
        #     if((t+1) % 5 == 0):
        #         if(t != prev_total_time):
        #             three = (random.randint(1,10) > 5)
        #             four = (random.randint(1,10) > 5)
        #             server.setblocking(True)
        #             clients[ID].send(pickle.dumps([33, three, four]))
        #             clients[ID].send(pickle.dumps([33, three, four]))
        #             clients[ID].send(pickle.dumps([33, three, four]))
        #             clients[ID].send(pickle.dumps([33, three, four]))
        #             clients[ID].send(pickle.dumps([33, three, four]))
        #             clients[not ID].send(pickle.dumps([33, three, four]))
        #             clients[not ID].send(pickle.dumps([33, three, four]))
        #             clients[not ID].send(pickle.dumps([33, three, four]))
        #             clients[not ID].send(pickle.dumps([33, three, four]))
        #             clients[not ID].send(pickle.dumps([33, three, four]))
        #             print('sent recipe')
        #     prev_total_time = t

        server.setblocking(False)
        # print(count)
        
        
        
        # print("Server data from client:", str(ID), ",", str(data),
        #       "||", str(temporary_data[0]), ",", str(temporary_data[1]))
        
    pass

# %% Control Loop
clients = []
player_names = []
temporary_data = [None, None]
game_scores = [0, 0, 0, 0]
# count = 0
while True:
    # Listen for client connections
    client, address = server.accept()
    
    # Update the count of threaded processes
    config["Thread_Count"] += 1
    
    # Print confirmation addresses of the connection
    print("Connected to", str(address[0]), ":", str(address[1]))
    
    # Store each connection
    clients.append(client)
    player_names.append(pickle.loads(client.recv(HEADER))[1])
    
    # Begin new threaded process for each player
    if (config["Thread_Count"] == 2):
        # Send the true condition
        clients[0].send(pickle.dumps(True))
        clients[1].send(pickle.dumps(True))
        
        # Wait for ready signal from BOTH PLAYERS
        # ready1 = get_data(clients[0])
        # ready2 = get_data(clients[1])
        ready1 = pickle.loads(clients[0].recv(config["HEADER"]))
        ready2 = pickle.loads(clients[1].recv(config["HEADER"]))

        # server.setblocking(False)
        time.sleep(1)
        # Send confirmation for synchronized start
        print('ready recev')
        
        clients[0].send(pickle.dumps(ready1))
        clients[1].send(pickle.dumps(ready2))

        print('send start back')

        if(ready1[0] == '0'):
            clients[0].send(pickle.dumps("ClientID: 0"))
            clients[1].send(pickle.dumps("ClientID: 1"))
        else:
            clients[1].send(pickle.dumps("ClientID: 0"))
            clients[0].send(pickle.dumps("ClientID: 1"))

        print('sent both')
        
        start_time = time.perf_counter()

        # print(count)
        
        start_new_thread(threaded_client, (clients, 0, temporary_data, start_time))
        start_new_thread(threaded_client, (clients, 1, temporary_data, start_time))
        # count += 1
    pass

