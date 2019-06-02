####### Command handler #######
### Author : Jisook Kim
### Date : May 2019

# TCP connection adding.
# Serial(RS232) connection adding.
# Video switch file read/write.

import socket
import time
import serial
import json


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


### Video switch file - read / write
class Video_Switch_File :
    def __init__(self) :
        self.in_num = 0
        self.out_num = 0
        self.file_name = "default file name"
        self.raw_data = None
        self.switcher_data = None
        self.input_data = None
        self.output_data = None
        self.input_list = []
        self.output_list = []

    # File name: IP922 2x2
    def switch_file_open(self, f_name) :
        f_name += ".ksw"

        try :
            with open(f_name) as json_file :

                #print("\n------------- Raw data of json file ----------------")
     
                self.raw_data = json.load(json_file)
                #print(self.raw_data)

                self.switcher_data = self.raw_data["switcher"]
                #print("\n------------- Switcher Data ----------------")
                #print(self.switcher_data)
                #print("\n")

                self.in_num = self.switcher_data["n_in"]
                self.out_num = self.switcher_data["n_out"]
                self.file_name = self.switcher_data["name"]
                #print("--- input: %d   output: %d" %(self.in_num, self.out_num))
                #print("--- file name: ", self.file_name)

                self.input_data = self.switcher_data["inputs"]
                #print("\n------------- Input Data ----------------")
                #print(self.input_data)

                self.output_data = self.switcher_data["outputs"]
                #print("\n------------- Output Data ----------------")
                #print(self.output_data)
                #print("\n")

                self.input_list = []
                print("\n------------- Individual Input ----------------")
                for x in range(self.in_num) :
                    self.input_list.append(self.input_data[x])
                    print(self.input_list[x])

                self.output_list = []
                print("\n------------- Individual Output ----------------")
                for x in range(self.out_num) :
                    self.output_list.append(self.output_data[x])
                    print(self.output_list[x])
                print("--------------------------------------------------")

        except IOError as ex :
            print("Exception: ", ex)
        except :
            print("Something wrong...")


    def switch_file_write(self, f_name) :
        f_name += ".ksw" # name for writing file
        with open(f_name, 'w') as outfile :
            json.dump(self.raw_data, outfile)

    # First read file and then edit! Possible not to read first???
    def switch_file_edit(self, f_name) :
        # create switch data from json file.
        self.switch_file_open(f_name)
        print("\n")
        #f_name += ".ksw"

        print("===== Edit the switch file =====")

        while True :
            sw_in_out = input("- Enter \"input\" OR \"output\": ")
            if sw_in_out == "input" or sw_in_out == "output":
                break
            print("Wrong value entered!")

        while True :
            sw_id = input("- Enter \"id\" of the device: ")
            sw_id = int(sw_id) 
            if sw_in_out == "input" and sw_id <= self.in_num and sw_id > 0:
                break
            elif sw_in_out == "output" and sw_id <= self.out_num and sw_id > 0:
                break
            else :
                print("Wrong value entered!")
        sw_id_update = sw_id - 1
        
        if sw_in_out == "input" : # 1.input
            one_device = self.input_list[sw_id_update]
           
        elif sw_in_out == "output" : # 2.output
            one_device = self.output_list[sw_id_update]
            
        print("--- Selected device info: ", one_device)

        print("- What data do you want to edit?")
        print("1. IP address  2. Device Name  ")
        edit_data = input("Enter number: ")
        edit_data = int(edit_data)

        if edit_data == 2 :
            sw_name = input("- Enter name you want to change: ")
            one_device["name"] = sw_name
            print(one_device["name"])
        elif edit_data == 1 :
            sw_ip = input("- Enter ip address you want to change: ")
            one_device["host"] = sw_ip
            print(one_device["host"])
            
        print("--- Changed device info: ", one_device)            
            
        ## OverWrite file name
        self.switch_file_write(f_name)
        print("- Changed info is saved to the file, \"", f_name, "\"")
        
            

### Switch test
class Switch_Test(Video_Switch_File, Tcp_Control) :
    def __init__(self) :
        self.in_num = 0
        self.out_num = 0
        self.input_list = []
        self.output_list = []
        self.file_name = "default file name"

    def v_file_read(self, file_name) :
        print("Trying to open json file of video switch, file_name=", file_name)
        self.switch_file_open(file_name)
        
    def v_file_write(self, file_name) :
        print("Trying to write json file of video switch, file_name=", file_name)
        self.switch_file_write(file_name)
        
    def v_file_edit(self, file_name) :
        self.switch_file_edit(file_name)

    def switch_command_run(self, none) :
        # individual switching command execute by user input
        if self.in_num == 0 or self.out_num == 0 :
            #print("Error. Enter the correct video file name.")
            print("To start sending a switching command,")
            print("FIRST open a video switch file. Enter \"read ksw (file name)\"")
            print("After reading the file, enter \"auto switch\"")
        else :
            print("get command from user - connect tcp - receive/send command - want to send more?")
              # get a switching command - run - ...
    
    
    def auto_switch(self, none) :
        if self.in_num == 0 or self.out_num == 0 :
            #print("Error. Enter the correct video file name.")
            print("To start auto switching,")
            print("FIRST open a video switch file. Enter \"read ksw (file name)\"")
            print("After reading the file, enter \"auto switch\"")

        else :
            # switching start.
            input_num = 1

            while True:
                
                for x in self.input_list :
                    ip = x["host"]
                    print("\n",x["sysid"], ip)
                    
                    cmd = "\rSPOASI%02d\r" % input_num
                    str_out = []
                
                    # tcp connect
                    self.ip_address = ip
                    self.tcp_control_connect()

                    time.sleep(0.5)
                    self.tcp_receive(str_out)
                    if len(str_out) != 0 :
                        print(str_out[0], end="")

                    self.tcp_send(cmd)
                    time.sleep(3)

                    str_out = []
                    self.tcp_receive(str_out)
                    if len(str_out) != 0 :
                        print(str_out[0], end="")

                    #if self.tcp_connected == 1 :
                    self.tcp_close() # close tcp
                    time.sleep(0.5)

                    if input_num >= 8 :
                        input_num = 1
                    else :
                        input_num += 1
            
            

##### class: switch command #####
#### switch command "SI", "SA", "SB" have dictionary to call each function
# SPO 01 SI 02
# SPO 01 SA 02
# SPO 01 SB 02

class comm_switch:
    def __init__(self, sw_com):
        self.sw_com = sw_com
        
        self.list_switch_type = ["SI", "SA", "SB"]
        
        self.input_command = { "SI": self.si_switch,
                               "SA": self.sa_switch,
                               "SB": self.sb_switch }
        self.out_num = 0
        self.in_num = 0
        self.switch_type = ""  # "SI", "SA", "SB"

        
    def run_command(self):
        minus = 0 # check if minus value
        temp = self.sw_com.strip() # remove space the front
        for x in self.list_switch_type:
            sw_list = temp.split(x)
            if len(sw_list) == 2:   # check if "SI", "SA", "SB"
                self.switch_type = x
                self.out_num = int(sw_list[0]) # SPOxx 
                self.in_num = int(sw_list[1])   # SIyy
                if self.out_num < 0 or self.in_num < 0: # check minus value
                    minus = 1
                    break
                break
        if self.switch_type != "" and minus == 0:
            message_call = self.input_command[self.switch_type]
            message_call(self.out_num, self.in_num)
            print(self.out_num, self.in_num)
        else:
            print("Wrong command!")
            
    #### functions of input_command, "SI", "SA", "SB"
    def si_switch(self, out_n, in_n):
        print("Audio and Video Output %02d switched to Input %02d." %(self.out_num, self.in_num))

    def sa_switch(self, out_n, in_n):
        print("Audio Only Output %02d switched to Input %02d." %(out_n, in_n))
    
    def sb_switch(self, out_n, in_n):
        print("Video Only Output %02d switched to Input %02d." %(out_n, in_n))
       

    

##### Serial (RS232) Control Connection #####
### connect / send / receive / close
class Serial_Control :
    def __init__(self) :
        self.serial_b_rate = 57600
        self.serial_port = "COM1"
        self.serial_bytesize = 8
        self.serial_connected = 0 # add into other cls!!!
        self.serial_obj = None

    def serial_control_connect(self) :
        try :         
            self.serial_obj = serial.Serial(port = self.serial_port,
                              baudrate = self.serial_b_rate,
                              bytesize = self.serial_bytesize,
                              timeout = 0.1)
            self.serial_obj.close() # necessary??? before open? yes. 
            print("Opening serial port...")
            self.serial_obj.open()
            print("Success in Serial connection")
            self.serial_connected = 1
        except :
            print("Error for Serial connection")
            self.serial_connected = 0  # connection Error
            self.serial_close()
            
    def serial_close(self) :
        if self.serial_connected == 1 :
            print("Serial Port Disconnected.")
            self.serial_obj.close()
            self.serial_connected = 0
            self.serial_obj.__del__()

    def serial_send(self, serial_data) :
        if self.serial_connected == 1 :
            self.serial_obj.write(serial_data.encode())
            time.sleep(0.2)

    def serial_receive(self, serial_data) :
        if self.serial_connected == 1 :
             while True :
                try :
                    #print("----Response from device----")
                    new_data = self.serial_obj.read(256).decode()
                    if new_data == "" :
                        break
                    else :
                        print(new_data, end="")
                except :
                    print("Error receive.")


### Serial Class for setting properties, call connect method
# Inherit from Serial_Control
class Serial_cls(Serial_Control) :
    def __init__(self) :
        self.serial_b_rate = 57600
        self.serial_port = "COM1"
        self.serial_bytesize = 8
        self.serial_connected = 0
        self.serial_obj = None

    def serial_baud(self, b_rate) :
        try :
            temp = int(b_rate)
            if temp > 0 :
                self.serial_b_rate = temp
                print("Serial(RS232) Baud rate is", self.serial_b_rate)
            else :
                print("Error! Wrong baudrate.")
        except :
            print("Error! Wrong baudrate.")

    def serial_port(self, s_port) :
        #COM2
        begin_index = s_port.find("COM")
        if begin_index >= 0 :
            find_num = s_port[begin_index + len("COM"):]
            try :
                temp = int(find_num)
                self.serial_port = s_port
                print("Serial(RS232) port is", self.serial_port)
            except :
                print("Error! Wrong port.")

    def serial_bytesize(self, s_byte) :
        try :
            temp = int(s_byte)
            if temp > 0 :
                self.serial_bytesize = temp
                print("Serial(RS232) byte size is", self.serial_bytesize)
            else :
                print("Error! Wrong baudrate.")
        except :
            print("Error! Wrong byte size.")

    # connect - serial port
    # serial - send first then receive.
    def serial_connect(self, none) :
        self.serial_control_connect()
        if self.serial_connected == 1 :
            while True :
                str_out = []
                str_com = input("")
                if str_com == "exit" :
                    break
                else :
                    str_com += "\r"
                self.serial_send(str_com)
                self.serial_receive(str_out)
            self.serial_close()

                    




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
        

##### class: help command #####
class Help :
    def __init__(self) :
        self.my_help = "my help"

    # remove one more space between string
    # ip     address  --> ip address
    def run_help(self, str_in) :
        if str_in == "": # help
            print("Help ALL")
            print("\n=============== HELP ===============")
            print(" status : see all status of the device.")
            print(" print : see all values of member variables.")
            print("--------------------------------------")
            print(" set ip address xxx.xxx.xxx.xxx   (xxx:0-255 range)")
            print(" tcp port xx  (xx : tcp port number)")
            print(" connect tcp : connect TCP")
            print("--------------------------------------")
            print(" serial baudrate xxxxx  (xxxxx:")
            print(" serial port xx  (xx: port number)")
            print(" serial bytesize x  (x: 7 or 8)")
            print(" connect serial : connect serial port")
            print("--------------------------------------")
            print(" read ksw (video switch file name) : read video switch file")
            print(" write ksw (video switch file name) : write video switch file")
            print(" edit ksw (video switch file name) : edit video switch file")
            print(" auto switch : auto switching based on video file")
            print(" switch : send switching commands")
            print("======================================\n")

        else : # help ip address, help tcp port...
            space = 0
            com_in = ""
            for x in str_in :
                if x == " " :
                    if space == 0 :
                        space = 1
                    else :
                        x = ""
                com_in += x
          
#            space = 0
#            com_in = ""
#            for x in str_in:
#                if x == " " :
#                    if space == 0 :
#                        space = 1
#                        com_in += x
#                    else :
#                        pass
#                else :
#                    com_in += x
#                    space = 0
                    
            print (com_in)  # complete string of command     
            com_len = len(com_in)
            for x in help_list_command:
                begin_index = com_in.find(x)
                list_com_len = len(x)
                if ( begin_index == 0 ) and ( com_len == list_com_len ) :
                    cls_call = help_list_command[x] # get addr of class (comm_help) = dic's value
                    cls_call(self) # call a class
                    break

        
    def help_ip(self) :
        print("To enter ip address, type this:")
        print("ip address xxx.xxx.xxx.xxx   (xxx : 0 - 255 range)")

    def help_tcp_port(self) :
        print("To enter tcp port, type this:")
        print("tcp port xx   (xx : tcp port number)")

        
help_list_command = { "ip address": Help.help_ip,
                      "tcp port": Help.help_tcp_port }
              


##### class: status command #####
class Status :
    def __init__(self) :
        self.my_status = "my status"
        
    def run_status(self, none) :
        print("=============== Status =================")
        print(" RS232 : Baud Rate=%dbps, Data=%dbit, Parity=None, Stop=1bit"
              %(self.serial_b_rate, self.serial_bytesize))
        print(" Serial Port = ", self.serial_port)
        print("-----------------")
        print(" Network Setting(Telnet Server) Status")
        print(" Host IP Address = ", self.ip_address)        
        print(" TCP Port = ", self.tcp_port)
        print("-----------------")
        




###### Command handle part ######
### Inherit from Help, Status, Network (parent class)
class Command(Help, Status, Terminal, Serial_cls, Switch_Test) :
    def __init__(self) :
        self.my_help = "help"
        self.my_status = "status"
        self.ip_address = "192.168.1.239"
        self.tcp_port = 23
        self.serial_b_rate = 57600
        self.serial_port = "COM1"
        self.serial_bytesize = 8
        self.tcpsock = None
        self.tcp_connected = 0
        self.serial_connected = 0
        self.serial_obj = None

        # need??? if want to show in status
        self.in_num = 0
        self.out_num = 0
        self.file_name = "default file name"
        self.raw_data = None
        self.switcher_data = None
        self.input_data = None
        self.output_data = None
        self.input_list = []
        self.output_list = []



       
        print("\n======== Command List ========")
        print(" help\n help ip address\n help tcp port")
        print(" status")
        print(" print")
        print("-------------------------------")
        print(" ip address xxx.xxx.xxx.xxx")
        print(" tcp port xx")
        print(" connect tcp")
        print("-------------------------------")
        print(" serial baudrate xxxxx")
        print(" serial port xx")
        print(" serial bytesize x")
        print(" connect serial")
        print("-------------------------------")
        print(" read ksw (file name)")
        print(" write ksw (file name)")
        print(" edit ksw (file name)")
        print(" auto switch")
        print(" switch")
        print("==============================\n")

    def print_all(self, none) :
        print("--- Default member variables ---")
        print(" help:", self.my_help)        
        print(" status:", self.my_status)
        print(" ip address:", self.ip_address)        
        print(" tcp port:", self.tcp_port)
        print(" serial baudrate:", self.serial_b_rate)
        print(" serial port:", self.serial_port)
        print(" serial bytesize:", self.serial_bytesize)


    ##### command handler to check which command entered by a user
    def command_handler(self) :
        str_com = ""
        str_com = input("JK > ")
        #str_com_len = len(str_com) 
        for x in list_command:
            begin_index = str_com.find(x)
            #list_com_len = len(x)
            if begin_index == 0 :
                cut_right = str_com[begin_index + len(x):] #get word after cmd for parameter of function
                #print(cut_right.strip())
                cls_call = list_command[x] # get addr of class (comm_help) = dic's value
                cls_call(self, cut_right.strip()) # call a class having argument
                break
        if (begin_index != 0) & (str_com != ""):
            print("Unknown Command. Enter \"help\" for usage of command.")

list_command = { "help": Help.run_help,
                 "status": Status.run_status,
                 
                 "ip address": Terminal.ip_address,
                 "tcp port": Terminal.tcp_port,
                 "connect tcp": Terminal.tcp_connect,
                 
                 "serial baudrate": Serial_cls.serial_baud, # data,parity,stop bits
                 "serial port": Serial_cls.serial_port,
                 "serial bytesize": Serial_cls.serial_bytesize,
                 "connect serial": Serial_cls.serial_connect,
                 
                 "print": Command.print_all,
                 
                 "read ksw" : Switch_Test.v_file_read,
                 "write ksw" : Switch_Test.v_file_write,
                 "edit ksw" : Switch_Test.v_file_edit,

                 "auto switch" : Switch_Test.auto_switch,
                 "switch" : Switch_Test.switch_command_run }


######### MAIN ########      
comm = Command()

while True :
    comm.command_handler()
    
   
