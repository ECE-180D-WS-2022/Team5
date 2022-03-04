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
host = "131.179.51.146" # IPv4 address of the Eng. IV lab room
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
except socket.error as e:
    print("Our error message:", str(e))
    
# %% Run Game
condition = pickle.loads(client.recv(HEADER))
    
if (condition[0] == True):
    print("Server has given the go-ahead!")
    while True:
        # Run the game logic with the client socket connection
        game(client)
        pass