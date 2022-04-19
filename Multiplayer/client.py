# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 13:33:28 2022

@author: Kellen Cheng
"""

# Import Statements
import pickle
import socket
from building_blocks import *

# %% Client Configuration
config = dict()
config["Host"] = "192.168.1.91" # IPv4 address of ENG IV lab room
config["Port"] = 4900 # Unique ID, can be any number but must match server's
config["HEADER"] = 4096 # Defines max number of byte transmission

# %% Client Setup
# Create the client socket
client = socket.socket()

# Connect the client online
try:
    client.connect((config["Host"], config["Port"]))
    print("STATUS -> Client bound successfully!")
    
except socket.error as e:
    print("ERROR ->", str(e))
    
# Remove blocking synchronous clients in favor of realtime nonblocking logic
client.setblocking(False)

# %% Client Methods
# Function : Threading function that checks for messages in the backround
def check_server(client):
    prev_message = None
    
    # Continuously check for received data
    while True:
        data = get_unblocked_data(client)
        
        # Print received data, if it exists
        if (data != None and data != prev_message and type(data) == list):
            prev_message = data
            print("SERVER SENDS -> " + str(prev_message))
        elif (data != None and type(data) == float):
            print("TIMER -> " + str(data))

# Function : Temporary game loop for prototype purposes
def temp_game(client):
    # Set a dedicated thread for checking for server messages
    input_thread = threading.Thread(target=check_server, 
                                    args=(client, ), 
                                    daemon=True)
    input_thread.start()
    
    # Temporary game loop
    while True:
        temp_data = input("Type something: ")
        
        # Send the data over to the server
        client.send(pickle.dumps(temp_data))
        
    pass

# %% Control Loop
condition = False
while (condition != True):
    try: condition = pickle.loads(client.recv(HEADER))
    except: condition = None
    pass

while True:
    temp_game(client)
    











