
import json
from Terminal_module import *


### Video switch file (json file) - read / write
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
