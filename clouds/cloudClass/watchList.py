import os
from time import sleep
import threading

class watchList:
    def __init__(self):
        self.init()
        self.__index = 0
        self.mod= []
        
    def init(self):
        self.__hash = {}
        self.__initFolders()
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
            
            
    
    def size(self):
        return len(self.__hash)
       
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
   
    
    def folderMtime(self, folder):
        return self.__hash[folder][0]
    
    def fileMtime(self, folder, index):
        return self.__hash[folder][index][0]
    
    def getFolders(self):
        return self.__hash.keys()
    
    def getFiles(self, folder):
        return self.__hash[folder][1:]
    
    def next(self):
        self.__index +=1 
        if self.__index>len(self.__hash.keys())-1:
            self.__index = 0
        return self.__hash.keys()[self.__index]
    
    def __diff(self, list1, list2):
        if len(list1)>= len(list2):
            diff = list(set(list1)-set(list2))
        else:
            diff =  list(set(list2)-set(list1))
        return diff
    
    def __updateHash(self):
        while True:
            for key in self.__hash.keys():
                if self.__hash[key][0]!=self.mTime(key):
                    self.init()
            sleep(5)
    
    def modified(self):
        while True:
            folder = self.next()
            for file in self.getFiles(folder):
                if file[0]!=self.mTime(folder+'/'+file[1]):
                    self.mod.append((folder+'/'+file[1]))
                    self.addFile(file[1], folder)
                    self.__hash[folder].remove(file)
            sleep(5)    
  
  
List = watchList()
List.printList()
print "make change"
user = str(raw_input())
threading.Thread(target = List.modified).start()
while user =='y':
    print List.mod
    user = str(raw_input())             