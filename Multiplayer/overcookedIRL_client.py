# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 17:55:30 2022

@author: Kellen Cheng
"""

# Import Statements
import pickle
import socket
from building_blocks import *

'''
N.B. Refer to the below link for the base theory behind the code:
    https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/
'''

# %% Setup Socket Client
# Define client connection parameters
host = "131.179.50.229" # IPv4 address of the Eng. IV lab room
host = "192.168.1.91" # IPv4 address of my (K's) apartment
port = 4900 # Unique 4 digit code to verify socket connections
client = socket.socket()

# Define operation runtime parameters
HEADER = 4096 # Maximum number of bytes for data transmission, i.e. 4096 bytes

# %% Initialize Game Client
# Connect game client online
try:
    client.connect((host, port))
    print("Client connected to server successfully!")
    
    # Register a new player
    register(client, header=HEADER)
except socket.error as e:
    print("Our error message:", str(e))
    
# %% Run Game
# Set client as non-blocking to run loading animation + be async
client.setblocking(False)
try: condition = pickle.loads(client.recv(HEADER))
except: condition = None

# Run the loading screen animation in this loop
while (condition != True): 
    # Error when reading non-existent data, so use try-except
    try: condition = pickle.loads(client.recv(HEADER))
    except: condition = None
    pass
    
if (condition == True):
    print("Server has given the go-ahead!")
    
    # Wait for player input that player is ready to begin game
    ready = input("When you are ready, type anything:\n")
    client.send(pickle.dumps([ready])) # Send ready signal to game server
    
    # Block the game logic from running for a synchronized start time
    ready_condition = get_data(client)
    
    # Run the game logic with the client socket connection
    game(client)