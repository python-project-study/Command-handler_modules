## UDP Protocol connection

# UDP server part

# server / client : different port but use same server ip

import socket

server_address = "127.0.0.1"
#UDP_IP_ADDRESS = "localhost"
#server_address = ("localhost", 10000)
server_port = 8000
Message = "I am server."

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((server_address, server_port))

while True :
    print("waiting for client...\n")
    data, addr = serverSock.recvfrom(1024)
    print("from Client: %s" % data.decode())  # data = string data from client
    print("addr :", addr)  # addr = ip and port

    str_in = input("server >> ")
    serverSock.sendto(str_in.encode(), addr)  # send data to client address
# OR    clientSock.sendto(b'Message', addr)
