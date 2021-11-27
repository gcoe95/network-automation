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
            device_params={'name':'iosxr'}
        )
    
    def getInterfaces(self):
        with self.__createConnection() as con:
            response = con.get_config(source="candidate", filter=('subtree', '<interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"/>'))
        if response.ok:
            return (response.data_xml, 200)
        return (response.error.info, 500)
    
    def patchInterface(self):
        pass

    def createInterface(self):
        body = """<?xml version="1.0" encoding="UTF-8"?>
        <nc:config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
                <interface-configuration>
                    <active>act</active>
                    <interface-name>Loopback66</interface-name>
                    <interface-virtual />
                    <description>Created via NETCONF - GC</description>
                </interface-configuration>
            </interface-configurations>
        </nc:config>"""
        
        with self.__createConnection() as con:
            response = con.edit_config(config=body, target="candidate", default_operation='merge')
            con.commit()
        if response.ok:
            return (str(response), 200)
        return (response.error.info, 500)

    def deleteInterface(self):
        pass