import socket
try:
    import cpickle as pickle
except:
    import pickle
from mchar import *
from random import *


class Client(object):
    def __init__(self, Level, Name, Host="", Port=9999):
        self.level = Level
        self.host = Host
        self.port = Port
        self.name = Name + str(randrange(1000)).encode()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addrUser = {}

    def connect(self):
        self.socket.sendto(self.name, (self.host, self.port))

    def send(self, input):
        t = pickle.dumps(input)
        self.socket.sendto(t, (self.host, self.port))

    def receive(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                r = pickle.loads(data)
                for i in r:
                    if not i in self.addrUser:
                        print(addr, "client!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        self.addrUser[i] = True
                return r
            except socket.error:
                break
        return {}