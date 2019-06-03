## UDP Protocol connection

# UDP client part


import socket

server_address = "127.0.0.1"
#UDP_IP_ADDRESS = "localhost"
#server_address = ("localhost", 10000)
server_port = 8000
Message = "Hellpppp from client"


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("UDP Client connected.")


clientSock.sendto(Message.encode(), (server_address, server_port ))
# OR    clientSock.sendto(b'Message', (UDP_IP_ADDRESS, UDP_PORT ))

while True:

    print("waiting for server...\n")
    data, addr = clientSock.recvfrom(1024)
    print("from Server: %s" % data.decode()) # data = string data from client
    print("addr :", addr)  # addr = ip and port

    str_in = input("client >> ")
    clientSock.sendto(str_in.encode(), (server_address, server_port ))
    # send data to Server
