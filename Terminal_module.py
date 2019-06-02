
### TCP module ###

import socket
import time

##### TCP Control connection #####
### connect / send / receive / close
class Tcp_Control :
    def __init__(self) :
        self.ip_address = "192.168.1.299"
        self.tcp_port = 29
        self.tcp_connected = 0
        self.tcpsock = None
        
    def tcp_control_connect(self) :
        try:
            self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcpsock.settimeout(0.5)

            print("Trying to connect to", self.ip_address, "port", self.tcp_port)
            self.tcpsock.connect((self.ip_address, self.tcp_port))
            print("Success in TCP connection!")
            self.tcp_connected = 1
            time.sleep(0.5) ## Need??
 
        except socket.error as msg :
            print("Error for connection!")
            self.tcp_connected = 0  # Error connection
            self.tcpsock.close()

    def tcp_close(self) :
        if self.tcp_connected == 1 :
            print("TCP disconnected.")
            self.tcp_connected = 0
            self.tcpsock.shutdown(1)
            self.tcpsock.close()

        
    def tcp_send(self, tcp_data) :
        if self.tcp_connected == 1 :
            self.tcpsock.send(tcp_data.encode())
            time.sleep(0.1)
            #print(tcp_data)
            
    def tcp_receive(self, tcp_data) :
        if self.tcp_connected == 1:
            self.tcpsock.settimeout(0.1)
            data = []
            try :
                cont = True
                while cont :
                    new_data = self.tcpsock.recv(64)
                    if not new_data :
                        cont = False
                    data.append(new_data)
            except:
                pass
            #print(data)
            print("\n")
            temp_data = b''.join(data)
            temp_tcp = ""
            for x in temp_data :
                if x < 0x80 :
                    temp_tcp += "%c" % x
            tcp_data.append(temp_tcp)
            #print(tcp_data)


### Network Class for setting properties, call connect method
### Inherit from TCP_Control (parent class)
class Terminal(Tcp_Control) :
    def __init__(self) :
        self.ip_address = "192.168.1.299"
        self.tcp_port = 29
        self.tcpsock = None
        self.tcp_connected = 0

    # set and check valid IP address 
    def ip_address(self, ip) :
        ip_list = ip.split(".")
        if len(ip_list) == 4 : # xxx.xxx.xxx.xxx (4 addr)
                range_ck = True
                ip_addr = []
                for x in ip_list :
                    addr = int(x)
                    if addr < 0 or addr > 255 :
                        print("Invalid address! (Must be 0-255 range)")
                        range_ck = False
                        break
                    ip_addr.append(addr)
                if range_ck == True :
                    print( "IP Address is ", end="" )
                    for x in range(3) :
                        print("%d" % ip_addr[x], end=".")
                    print("%d" % ip_addr[3])
                    self.ip_address = ip # store ip address as a string
        else:
            print("Invalid address! (Must be xxx.xxx.xxx.xxx)")

    # check valid tcp port
    def tcp_port(self, tcp_port) :
        try:
            temp = int(tcp_port)
            if temp > 0 :
                self.tcp_port = temp
                print("TCP Port number is", self.tcp_port)
            else:
                print("Error! Must be positive number.")
        except:
            print("Error! Must be Integer.")

    # connect - tcp
    # tcp - receive first then send.
    def tcp_connect(self, none) :
        self.tcp_control_connect()
        if self.tcp_connected == 1 :
            str_out = []
            self.tcp_receive(str_out)
            print(str_out[0], end="")
                
            while True :
                str_com = input("")
                if str_com == "exit" :
                    #self.tcp_close()
                    break
                else :
                    str_com += "\r"
                self.tcp_send(str_com)
                str_out = []
                self.tcp_receive(str_out)
                print(str_out[0], end="")
            self.tcp_close() # close tcp
