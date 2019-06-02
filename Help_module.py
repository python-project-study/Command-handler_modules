### --- Help module


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
