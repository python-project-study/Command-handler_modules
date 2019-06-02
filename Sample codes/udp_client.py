## UDP Protocol connection

# UDP client part

import socket

UDP_IP_ADDRESS = "127.0.0.2"
#UDP_IP_ADDRESS = "localhost"
#server_address = ("localhost", 10000)
UDP_PORT = 8000
Message = "Hellpppp from client"


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("UDP Client connected.")
print("UDP target Port: ", UDP_PORT)

clientSock.sendto(Message.encode(), ("127.0.0.1", UDP_PORT ))
# OR    clientSock.sendto(b'Message', (UDP_IP_ADDRESS, UDP_PORT ))

while True:
    data, addr = clientSock.recvfrom(1024)

    print("Received Messages from SERVER: ", data.decode())
    print("from :", addr)

