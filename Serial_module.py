
### Serial module ###

import time
import serial


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
                    

