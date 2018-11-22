import socket
import time
import threading

class client:
    def __init__(self,socket_type,server_IP,server_port):
        self.TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_type = socket_type
        self.server_IP = server_IP
        self.server_port = server_port
        self.input_msg = ''
        self.buffer_size = 4096
        self.bdata = ''
        self.dcmsg = '-CLIENT-LEAVING-'
        self.joinmsg = '-CLIENT-JOINED-'
        self.tooltip = '(Enter messages or -q to quit)'
        if (self.socket_type == 'UDP'):
            print(self.tooltip)
            self.UDP.sendto(self.encode_string(self.joinmsg),\
            (self.server_IP,self.server_port))
            self.bdata = self.decode_bytes(self.UDP.recvfrom(self.buffer_size)[0])
            if self.bdata:print(self.bdata)
        else:
            self.TCP.connect((self.server_IP, self.server_port))
            print(self.tooltip)
            self.TCP.sendall(self.encode_string(self.joinmsg))
            self.bdata = self.decode_bytes(self.TCP.recv(self.buffer_size))
            if self.bdata:print(self.bdata)
    
    def encode_string(self,string):return str.encode(string,"utf-8")
    
    def decode_bytes(self,byte):return byte.decode("utf-8") 
    
    def tcp_send_commands(self):
        while (True):
            self.input_msg =input()
            if self.input_msg =='-q': 
                self.TCP.sendall(self.encode_string(self.dcmsg))
                self.endsession = self.decode_bytes(self.TCP.recv(self.buffer_size))
                if self.endsession:print(self.endsession)
                break
            self.TCP.sendall(self.encode_string(self.input_msg))
            self.data = self.decode_bytes(self.TCP.recv(self.buffer_size))
            if self.data:print(self.data)
        self.TCP.close()
        
    def udp_send_commands(self):
        while (True):
            self.input_msg = input()
            if self.input_msg == '-q': 
                self.UDP.sendto(self.encode_string(self.dcmsg),\
                (self.server_IP,self.server_port))
                while (True):
                    self.endsession = self.decode_bytes(\
                    self.UDP.recvfrom(self.buffer_size)[0])
                    if self.endsession:print(self.endsession)
                    self.UDP.close()
                    exit()
            else:
                self.UDP.sendto(self.encode_string(self.input_msg),\
                (self.server_IP,self.server_port))
                self.response = self.decode_bytes(\
                self.UDP.recvfrom(self.buffer_size)[0])
                if self.response:print(self.response)
                
    def connect(self):
        if self.socket_type == 'UDP':
            threading.Thread(target=self.udp_send_commands()).start()
        if self.socket_type == 'TCP':
            threading.Thread(target=self.tcp_send_commands()).start()
    
    
mainhallclient = client('TCP','192.168.1.1', 4444)
mainhallclient.connect()