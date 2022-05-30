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
from threading import Lock
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

acks = [[[None, None, None, None],[1, 1, 1, 1]], [[None, None, None, None],[1, 1, 1, 1]]]
ack_time = 2500
ack_messages = [{}, {}, {}, {}]
ack_counts = [1,1,1,1]

lock = Lock()

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
    global acks

    # shared_station_free_66 = None
    # shared_station_pass_99 = None
    # score_88 = None
    # recipe_33 = None
    # vals = [None, None, None, None]
    # counts = [1, 1, 1, 1]
    # count_33 = 0
    # count_66 = 0
    # count_99 = 0
    # count_88 = 0
    # count = -10

    while True:
        # count += 0
        data = get_unblocked_data(clients[ID])
        if(data != None):
            print(data)
            print(str(ID) + "- sdfsdfsdf " + str(data[0]))

        
        if (type(data) == list and len(data) != 0 and data[0] == 22):
                clients[not ID].send(pickle.dumps(data))
        elif (type(data) == list and len(data) != 0 and data[0] == 99):
            # Sending item to the other player!
            print("Sending data1------------------------")
            print("Received:", str(data))
            # key = len(shared_station_pass_99)
            # key = 0
            # new_data = data.append(key)
            # clients[not ID].send(pickle.dumps(new_data))
            # shared_station_pass_99[key] = new_data
            shared_station_pass_99 = data
            lock.acquire()
            acks[ID][0][0] = data
            lock.release()
            clients[not ID].send(pickle.dumps(data))
            print("ID:", str(ID), "and not ID:", str(not ID))
            print("Client0:", str(clients[0]), ", Client1:", str(clients[1]))
        elif (type(data) == list and len(data) != 0 and data[0] == 88):
            print('score update --------------------------------------------')
            # We need to update scores!
            # Code for updating scores!
            game_scores[ID] = data[1]
            # Send the score to all other players
            # key = len(score_88)
            # key = 0
            # new_data = data.append(key)
            # clients[not ID].send(pickle.dumps(new_data))
            # score_88[key] = new_data
            score_88 = data
            lock.acquire()
            acks[ID][0][1] = data
            lock.release()
            clients[not ID].send(pickle.dumps(data))
            pass
        elif (type(data) == list and len(data) != 0 and data[0] == 66):
            # We need to set a share station to be unoccupied!
            print('shared station free -----------------------------------')
            # key = len(shared_station_free_66)
            # key = 0
            # new_data = data.append(key)
            # clients[not ID].send(pickle.dumps(new_data))
            # shared_station_free_66[key] = new_data
            shared_station_free_66 = data
            lock.acquire()
            acks[ID][0][2] = data
            lock.release()
            clients[not ID].send(pickle.dumps(data))
        elif (type(data) == list and len(data) != 0 and data[0] == 33):
            print('recipe gen received--------------------')
            # key = len(recipe_33)
            # key = 0
            # new_data = data.append(key)
            # clients[not ID].send(pickle.dumps(new_data))
            # recipe_33[key] = new_data
            recipe_33 = data
            lock.acquire()
            acks[ID][0][3] = data
            lock.release()
            clients[not ID].send(pickle.dumps(data))
        elif (type(data) == list and len(data) != 0 and data[0] == 999):
            # del shared_station_pass_99[data[1]]
            shared_station_pass_99 = None
            lock.acquire()
            acks[not ID][0][0] = None
            acks[not ID][1][0] = 1
            lock.release()
        elif (type(data) == list and len(data) != 0 and data[0] == 888):
            # del score_88[data[1]]
            score_88 = None
            lock.acquire()
            acks[not ID][0][1] = None
            acks[not ID][1][1] = 1
            lock.release()
        elif (type(data) == list and len(data) != 0 and data[0] == 666):
            # del shared_station_free_66[data[1]]
            shared_station_free_66 = None
            lock.acquire()
            acks[not ID][0][2] = None
            acks[not ID][1][2] = 1
            lock.release()
        elif (type(data) == list and len(data) != 0 and data[0] == 333):
            # del recipe_33[data[1]]
            print(str(ID) +'we should be done here ----------------------------:' + str(acks[not ID][1][3]))
            recipe_33 = None
            lock.acquire()
            acks[not ID][0][3] = None
            acks[not ID][1][3] = 1
            lock.release()
            # print(str(ID) + vals[3])
            print(str(ID) + '-' + str(acks[not ID][1][3]))
            print(str(ID) + 'we should be done here ----------------------------2')
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

        lock.acquire()
        if(acks[ID][0][0]):
            if(acks[ID][1][0] % ack_time == 0):
                clients[not ID].send(pickle.dumps(acks[ID][0][0]))
                acks[ID][1][0] = 0
            acks[ID][1][0] += 1
        if(acks[ID][0][1]):
            if(acks[ID][1][1] % ack_time == 0):
                clients[not ID].send(pickle.dumps(acks[ID][0][1]))
                acks[ID][1][1] = 0
            acks[ID][1][1] += 1
        if(acks[ID][0][2]):
            if(acks[ID][1][2] % ack_time == 0):
                clients[not ID].send(pickle.dumps(acks[ID][0][2]))
                acks[ID][1][2] = 0
            acks[ID][1][2] += 1
        if(acks[ID][0][3]):
            if(acks[ID][1][3] % ack_time == 0):
                print(acks[ID][1][3])
                print(acks[ID][0][3])
                print('we are sending data for some reaons')
                clients[not ID].send(pickle.dumps(acks[ID][0][3]))
                acks[ID][1][3] = 0
            acks[ID][1][3] += 1
        lock.release()
        
        # for key, val in shared_station_pass_99.items():
        #     clients[not ID].send(pickle.dumps(val))

        # for key, val in score_88.items():
        #     clients[not ID].send(pickle.dumps(val))

        # for key, val in shared_station_free_66.items():
        #     clients[not ID].send(pickle.dumps(val))

        # for key, val in recipe_33.items():
        #     clients[not ID].send(pickle.dumps(val))
        
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

