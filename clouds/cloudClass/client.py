from OpenSSL import SSL
import socket

                    
class client:
    def __init__(self, host, port, key, cert):
        self.buffer = 1024
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_privatekey_file(key)
        context.use_certificate_file(cert)
        self.clientSocket = SSL.Connection(context,self.clientSocket)
        self.address = (host, port)
        self.foldersToWatch()
    
    def connect(self):
        self.clientSocket.connect(self.address)
        self.status = self.clientSocket.recv(self.buffer)
        print self.status+"\n"
        
    def send(self, data):
        self.clientSocket.send(data)
    
    def recv(self):
        return self.clientSocket.recv(self.buffer)
    
    def transfer(self, file): #remember to test this code
        ofile = open(file)
        data = ofile.readline()
        while data !='':
            self.clientSocket.sendall()
            data = ofile.readline()
        ofile.close()
    
    def osCommand(self, command):
        terminal = sub.Popen(command,stdout=sub.PIPE,stderr=sub.PIPE)
        output, error = terminal.communicate()
        if error == '':
            return output
        else:
            return error

    def foldersToWatch(self):
        file = open('watchList.txt', 'r')
        self.line = file.readlines()
        if self.line == '':
            print 'No folders listed'
        else:
            print str(len(self.line))+' folders are being watched for changes'
            
    #def isedited(self, folder):
        
        
    def shutdown(self):
        self.clientSocket.close()
        
#c = client("127.0.0.1", 12345, 'key', 'cert')
#c.connect()



        
       