# import socket

# class Network:
#     def __init__(self):
#         self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server = "192.168.86.24"
#         self.port = 5555
#         self.addr = (self.server, self.port)
#         self.id = self.connect()
#         print(self.id)

#     def connect(self):
#         try:
#             self.client.connect(self.addr)
#             return self.client.recv(2048).decode()
#         except:
#             pass

arr = [100, 1, 2, 3]

print(arr[False])


import pickle
pickle.loads(None)



