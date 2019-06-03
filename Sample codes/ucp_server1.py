## UDP Protocol connection

# UDP Server part

import socket

UDP_IP_ADDRESS = "127.0.0.1"
#UDP_IP_ADDRESS = "localhost"
#server_address = ("localhost", 10000)

UDP_PORT = 8000
Message = "I am Server1"

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT))



while True :
    print("waiting for client...\n")
    data, addr = serverSock.recvfrom(1024)


    print("Received Messages from client: ", data.decode())
    print("from :", addr)

    str_in = input(">>> ")
    serverSock.sendto(str_in.encode(), ("127.0.0.1", 8001 )) #server2 Port
