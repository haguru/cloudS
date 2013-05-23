import sys
from OpenSSL import SSL 
import socket 
import thread

class server:
    def __init__(self):
        self.buffer = 1024
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ("", 12345)
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_privatekey_file('key')
        context.use_certificate_file('cert')
        self.serverSocket = SSL.Connection(context,self.serverSocket)
        

    
    def incomingConnection(self):
        client,addr =  self.serverSocket.accept()
        client.send("connected")
        #self.users.append(client)
        
        
    
    def start(self):
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.address[0] == "None" or self.address[1] == 0:
            print "Invalid address"
        else:
            self.serverSocket.bind(self.address)
            self.serverSocket.listen(5)
            self.incomingConnection()
    
    
    def shutdown(self):
        self.serverSocket.close()
        

#s = server()
#s.start()