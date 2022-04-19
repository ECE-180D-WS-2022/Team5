import socket
from _thread import *
import sys

server = "192.168.86.24"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server and port to socket
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("waiting for connection: server started")

def threaded_client(conn):
    conn.send(str.encode("Connected"))

    # run while client is still connected
    while True:
        try:
            # number of bits
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("disconnected")
                break
            else:
                print("received: ", reply)
                print("sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break
    print("lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))