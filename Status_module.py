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
