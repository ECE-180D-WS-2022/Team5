import socket
import pickle
from building_blocks import *
HEADER = 4096

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Game started, waiting for connection...')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(HEADER)
print(Response.decode('utf-8'))

count = 0
while True:
    game_start(ClientSocket)
    
    Input = input("Say Something: ")
    ClientSocket.send(pickle.dumps(Input))
    Response = pickle.loads(ClientSocket.recv(HEADER))
    Response1 = pickle.loads(ClientSocket.recv(HEADER))
    print(Response)
    print(Response1)
    
    count += 1

ClientSocket.close()