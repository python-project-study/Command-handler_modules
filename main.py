####### Command handler #######
### Author : Jisook Kim
### Date : May 2019
##############################
# TCP connection adding.
# Serial(RS232) connection adding.
# Video switch file(json) read/write.
# After reading, auto switch enabled


#import socket
import time
#import serial
#import json

# import all methods from module "Status_module.py", more modules below.
#from Status_module import *
#from Help_module import *
#from Serial_module import *
#from Terminal_module import *
#from Switch_module import *
from Command_module import *





######### MAIN ########
comm = Command()

while True :
    comm.command_handler()
