import subprocess as sub
import os
from OpenSSL import SSL
import socket

class watchList:
    def __init__(self):
        self.__hash = {}
        self.__initFolders()
        self.current = self.__hash.iterkeys()
        self.__initFiles()
        
    def __initFiles(self):
        for folder in self.__hash:
            files = os.listdir(folder)
            for file in files:
                self.addFile(file, folder)
                
    
    def __initFolders(self):
        with open("watchList.txt") as List:
            lines = List.readlines()
            for line in lines:
                Path = line[0:-1]
                if self.isDir(Path):
                    self.addFolder(Path)
                    for subDir in self.subFolder(Path):
                        self.addFolder(subDir)
            
            
    
        
    def log(self,data):
        log = open('log.txt', 'a+')
        log.write(data+'\n')
        
        
    def printList(self):
        print self.__hash
        self.log(str(self.__hash))
        
    def isDir(self, file):
        return os.path.isdir(file)
    
    def mTime(self, path):
        return os.path.getmtime(path)
    
    
    def addFolder(self,folder):
        if not self.__hash.has_key(folder):
            self.__hash[folder] = [self.mTime(folder)]
            self.current = self.__hash.iterkeys()
        else:
            return -1
        
    def subFolder(self, path):
        walk = os.walk(path)
        return [folder[0] for folder in walk]
                
                    
    def addFile(self, file, folder):
        if not file in self.__hash[folder] and not self.isDir(folder+'/'+file):
            self.__hash[folder].append((self.mTime(folder+"/"+file), file))
        
        else:
            return -1
   
    def contents(self, folder):
        if self.__hash.has_key(folder):
            return self.__hash[folder]
        else:
            return []
    
    def folderMtime(self, folder):
        return self.__hash[folder][0]
    
    def fileMtime(self, folder, index):
        return self.__hash[folder][index][0]
    
    def getFilename(self, folder, index):
        return self.__hash[folder][index][1]
    
    def getFiles(self, folder):
        list =  []
        for index in range(len(self.__hash[folder])):
            if index == 0:
                continue
            list.append(self.__hash[folder][index][1])
        return list
    
    def next(self):  
        return self.current.next()
    
    def __diff(self, list1, list2):
        if len(list1)>= len(list2):
            diff = list(set(list1)-set(list2))
        else:
            diff =  list(set(list2)-set(list1))
        return diff
    
    def updateHash(self):
        for folder in self.__hash.keys():
            #Does folder still exist
            print "Updating " + folder
            diff = self.__diff(os.listdir(folder), self.getFiles(folder))
            if diff == []:    
                continue
            else:
                for file in diff:
                    self.addFile(file, folder)
                    
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

List = watchList()
List.printList()
done = False
while not done:
    print "make change"
    user = str(raw_input())
    if user == 'y':
        List.updateHash()
        List.printList()
        done = True
        
        