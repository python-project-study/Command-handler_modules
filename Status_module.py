### --- Status module



##### class: status command #####
class Status :
    def __init__(self) :
        self.my_status = "my status"

    def run_status(self, none) :
        print("=============== Status ===================")
        print(" RS232 : Baud Rate=%dbps, Data=%dbit, Parity=None, Stop=1bit"
              %(self.serial_b_rate, self.serial_bytesize))
        print(" Serial Port = ", self.serial_port)
        print("------------------------------------------")
        print(" Network Setting(Telnet Server) Status")
        print(" Host IP Address = ", self.ip_address)
        print(" TCP Port = ", self.tcp_port)
        print("------------------------------------------")

        if self.in_num != 0 or self.out_num != 0 :
            print("\n----------- Info - Video switch file - \"Input\" ----------------")
            for x in range(self.in_num) :
                self.input_list.append(self.input_data[x])
                print("Input",self.input_list[x]["sysid"], ":", self.input_list[x])

            print("\n----------- Info - Video switch file - \"Output\" ---------------")
            for x in range(self.out_num) :
                self.output_list.append(self.output_data[x])
                print("Output",self.output_list[x]["sysid"], ":", self.output_list[x])
            print("-------------------------------------------------------------------")
