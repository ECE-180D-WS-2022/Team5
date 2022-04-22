# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 17:55:30 2022

@author: Kellen Cheng
"""

# Import Statements
import pickle
import socket
from building_blocks import *
from game import *

'''
N.B. Refer to the below link for the base theory behind the code:
    https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/
'''

# %% Setup Socket Client
# Define client connection parameters
host = "131.179.38.24" # IPv4 address of the Eng. IV lab room
# host = "192.168.1.91" # IPv4 address of my (K's) apartment
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
    # register(client, header=HEADER)
except socket.error as e:
    print("Our error message:", str(e))
    
# %% Run Game
g = Game(client, HEADER)
g.intro_screen()
g.new()

# condition = pickle.loads(client.recv(HEADER))
# if (condition == True):
#     print("Server has given the go-ahead!")
    
#     # Wait for player input that player is ready to begin game
#     ready = input("When you are ready, type anything:\n")
#     client.send(pickle.dumps([ready])) # Send ready signal to game server
    
#     # Block the game logic from running for a synchronized start time
#     ready_condition = pickle.loads(client.recv(HEADER))
while g.running:
    g.main()
    
while True:
    # Run the game logic with the client socket connection
    game(client)
    pass