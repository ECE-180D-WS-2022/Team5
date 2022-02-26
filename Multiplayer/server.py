import socket
import os
import pickle
from _thread import *
from building_blocks import *

# https://codezup.com/socket-server-with-multiple-clients-model-multithreading-python/

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
HEADER = 4096 # Upper cap on data sending limits

kitchen_stations = Station_Manager()

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Server started, waitiing for players..')
ServerSocket.listen(5) # Limit to 5 clients

# Player Thread
def threaded_client(connection):
    # Send new game message to player
    connection.send(str.encode('Welcome to Overcooked IRL!'))
    recipe = "Testing recipe of [fish, beans, chili peppers]"
    # N.B. Sendall can be used to display timer and notifications to everyone!
    
    count = 0
    player = None
    
    while True: # Probably modify this to incorporate game code
        data = pickle.loads(connection.recv(HEADER))
        reply = data
        
        if not data:
            break
        
        if (player == None):
            player = Player(data)
            connection.send(pickle.dumps("Confirmed player: " + data))
            connection.send(pickle.dumps("Here is your recipe: " + str(recipe)))
        else:
            process_action(kitchen_stations, player, data, connection)
            connection.send(pickle.dumps(reply))
            connection.send(pickle.dumps(player.location))
            
        print("Iteration: " + str(count))
        print("Player: " + str(player.name))
        print("Inventory: " + str(player.inventory))
        print("Location: " + str(player.location))
        print("Plate: " + str(player.plate))
        print("This iteration's data: " + str(data))
        print("##################################################")
        
        count += 1
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    # print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    # print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()