### --- Command module


from Status_module import *
from Help_module import *
from Serial_module import *
from Terminal_module import *
from Switch_module import *

###### Command handle part ######
### Inherit from Help, Status, Serial_cls, Terminal, Switch_Test (parent class)

### Necessary to inherit???? YES. Parents are from above modules
class Command(Help, Status, Serial_cls, Terminal, Switch_Test) :
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
        print(" help")
        print(" help ip address")
        print(" help tcp port")
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
        str_com = str_com.strip()
        for x in list_command:
            begin_index = str_com.find(x)
            #list_com_len = len(x)
            if begin_index == 0 :
                cut_right = str_com[begin_index + len(x):] #get word after cmd for parameter of function
                #print(cut_right.strip())
                cls_call = list_command[x] # get addr of class (comm_help) = dic's value
                cls_call(self, cut_right.strip()) # call a class having parameter
                break
        if (begin_index != 0) & (str_com != ""):
            print("Unknown Command. Enter \"help\" for usage of command.")


### Command list
list_command = { "help": Help.run_help,
                 "status": Status.run_status,

                 "ip address": Terminal.ip_address,
                 "tcp port": Terminal.tcp_port,
                 "connect tcp": Terminal.tcp_connect,

                 "serial baudrate": Serial_cls.serial_baud,
                 "serial port": Serial_cls.serial_port,
                 "serial bytesize": Serial_cls.serial_bytesize,
                 "connect serial": Serial_cls.serial_connect,

                 "print": Command.print_all,

                 "read ksw" : Switch_Test.v_file_read,
                 "write ksw" : Switch_Test.v_file_write,
                 "edit ksw" : Switch_Test.v_file_edit,

                 "auto switch" : Switch_Test.auto_switch }
