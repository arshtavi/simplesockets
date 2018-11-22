import socket
import datetime
import time
import threading

class server:
    def __init__(self,socket_type,server_IP,server_port):
        self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_type = socket_type
        self.server_IP = server_IP
        self.server_port = server_port
        self.logging_enabled = True
        self.log_path = 'log.txt'
        self.request_counter = 1
        self.buffer_size = 4096
        self.connections = 1
        self.dcmsg = '-CLIENT-LEAVING-'
        self.joinmsg = '-CLIENT-JOINED-'
        self.client_message = ''
        self.client_address= ''
        self.tcp_client_address=''
        self.client_IP = ''
        self.client_port =''
        self.tcp_client_data = ''
        self.msg_connected = 'CONNECTED'
        self.msg_disconnected = 'DISCONNECTED'
        self.welcomebanner = "~~~~~~~~~~~~~~~~~~~~~~~~~\n"+\
                             "Welcome To Arsh's server!\n"+\
                             "~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.endsession = "~~~~~~~~~~~~~~~~~~~~~~~~~\n"+\
                          "        Goodbye          \n"+\
                          "~~~~~~~~~~~~~~~~~~~~~~~~~"
                          
        if (socket_type == 'UDP'):
            self.UDP.bind((server_IP, server_port))
        else:
            self.TCP.bind((server_IP, server_port))
            self.TCP.listen(self.connections)
        

    def current_time_long(self):return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def current_time_short(self):return datetime.datetime.now().strftime("%H:%M:%S")
    
    def encode_string(self,string):return str.encode(string,"utf-8")
        
    def decode_bytes(self,byte):return byte.decode("utf-8") 
    
    def log(self,msg=''):
        if msg == '': msg = self.client_message
        if (self.logging_enabled):
            with open(self.log_path, "a") as s:s.write(\
            '{}|{}|{}|{}:{}|{}\n'.format(\
            self.request_counter,\
            self.socket_type,\
            self.current_time_long(),\
            self.client_IP,\
            self.client_port,\
            msg))
            s.close()
    
    def print_client_message(self,disconnected=False,connected=False):
        if connected: self.client_message = self.msg_connected
        if disconnected: self.client_message = self.msg_disconnected
        print("[{}][{}][{}:{}] {}".format(\
        self.socket_type,\
        self.current_time_short(),\
        self.client_IP,\
        self.client_port,\
        self.client_message))
        
    def client_response(self):
        self.response_text = "[{}][{}:{}] Message #{} Received.".format(\
        self.current_time_short(),\
        self.server_IP,\
        self.server_port,\
        self.request_counter)
        self.bytes = self.encode_string(self.response_text)
        self.request_counter += 1
        return self.bytes
    
    def read_client_message(self):
        if (self.socket_type)=='UDP':
            self.client_message = self.decode_bytes(self.udp_client_data[0])
            self.client_IP = self.udp_client_data[1][0]
            self.client_port = self.udp_client_data[1][1]
            self.client_address = (self.client_IP,self.client_port)
        else:
            self.client_message = self.tcp_client_data
            self.client_IP = self.tcp_client_address[0]
            self.client_port = self.tcp_client_address[1]
    
    
    def udp_server(self):
        while True:
            self.udp_client_data = self.UDP.recvfrom(self.buffer_size)
            
            if self.udp_client_data != '':
                self.read_client_message()  
                if self.client_message == self.dcmsg:
                    self.print_client_message(True,False)
                    self.log(self.msg_disconnected)
                    self.udp_client_data = ''
                    self.UDP.sendto(self.encode_string(self.endsession),self.client_address)    
                elif self.client_message == self.joinmsg:
                    self.print_client_message(False,True)
                    self.log(self.msg_connected)
                    self.udp_client_data = ''
                    self.UDP.sendto(self.encode_string(self.welcomebanner),self.client_address)     
                elif self.client_message:
                    self.print_client_message() 
                    self.udp_client_data = ''
                    self.UDP.sendto(self.client_response(),self.client_address)       
    
     
    def tcp_server(self):
        while(True):
            self.tcp_client,self.tcp_client_address = self.TCP.accept()
            while True:
                self.incoming_data = self.decode_bytes(\
                self.tcp_client.recv(self.buffer_size))
                if self.incoming_data == self.dcmsg:
                    self.print_client_message(True, False)
                    self.log(self.msg_disconnected)
                    self.tcp_client.sendall(self.encode_string(self.endsession))
                    self.tcp_client.close()
                    self = self.tcp_server()
                elif self.incoming_data == self.joinmsg:
                    self.read_client_message()
                    self.print_client_message(False, True)
                    self.log(self.msg_connected)
                    self.tcp_client.sendall(self.encode_string(self.welcomebanner))
                elif self.incoming_data:
                    self.tcp_client_data = self.incoming_data
                    self.read_client_message()
                    self.print_client_message()
                    self.tcp_client.sendall(self.client_response())
                else:
                    break
                    
    def start(self):
        if self.socket_type == 'UDP':threading.Thread(target=self.udp_server()).start()
        if self.socket_type == 'TCP':threading.Thread(target=self.tcp_server()).start()
    

yourserver = server('TCP','0.0.0.0', 4444)
yourserver.start()