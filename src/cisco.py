from ncclient import manager
from ncclient.xml_ import *

class Cisco:

    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = 830
        #self.connection = self.__createConnection()

    def __createConnection(self):
        return manager.connect(
            host=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            hostkey_verify=False,
            device_params={'name':'default'}
        )
    
    def getInterfaces(self):
        with self.__createConnection() as con:
            response = con.get(filter=('subtree', '<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"/>'))
        print(response.xml)
        return response
    
    def deleteInterface(self):
        pass

    def createInterface(self):
        pass

    def deleteInterface(self):
        pass