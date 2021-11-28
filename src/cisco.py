from ncclient import manager
from ncclient.xml_ import *
from netmiko import ConnectHandler

class Cisco:

    def __init__(self, hostname, username, password, dryRun=False):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.dryRun = dryRun

class CiscoNC(Cisco):

    def __init__(self, port, **kwargs):
        super(CiscoNC, self).__init__(**kwargs)
        self.port = port

    # Create a netconf connection to the device
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
        body = """<?xml version="1.0" encoding="UTF-8"?>
        <nc:config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
                <interface-configuration  nc:operation="delete">
                    <interface-name>Loopback66</interface-name>
                    <active>act</active>
                </interface-configuration>
            </interface-configurations>
        </nc:config>"""
        with self.__createConnection() as con:
            response = con.edit_config(config=body, target="candidate", default_operation='merge')
            con.commit()
        if response.ok:
            return (str(response), 200)
        return (response.error.info, 500)

class CiscoSSH(Cisco):

    def __init__(self, port, **kwargs):
        super(CiscoSSH, self).__init__(**kwargs)
        self.port = port

    def __createConnection(self):
        device = {
            'device_type': 'cisco_xr',
            'host': self.hostname,
            'username': self.username,
            'password': self.password,
            'port': 22,
        }
        return ConnectHandler(**device)

    def getInterfaces(self):
        commands = [
            "term len 0",
            "show ip int br"
        ]
        if self.dryRun: return commands
        with self.__createConnection() as con:            
            for cmd in commands:
                response = con.send_command(cmd) 
        return response