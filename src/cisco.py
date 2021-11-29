#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from ncclient import manager
from ncclient.operations.rpc import RPCError
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
    
    def getInterfaces(self):
        filterData = self.__getData("get_interfaces.xml", {}) 
        if self.dryRun: return(filterData, 200)
        with self.__createConnection() as con:
            try:
                response = con.get_config(source="candidate", filter=('subtree', filterData))
            except RPCError as e:
                return (e.xml, 400)
            except:
                return ("Internal Server Error", 500)
            if response.ok:
                return (response.xml, 201)
            return ("Internal Server Error", 500)

    def createInterface(self, params):
        try: body = self.__getData("loopback_create.xml", params) 
        except Exception as e: return (str(e), 400)       
        return self.__editConfig(body, "candidate")

    def deleteInterface(self):
        try: body = self.__getData("loopback_delete.xml", {"name": "Loopback66"}) 
        except Exception as e: return (str(e), 400) 
        return self.__editConfig(body, "candidate")

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

    def __editConfig(self, config, target, operation="merge"):
        if self.dryRun: return(config, 200)
        with self.__createConnection() as con:
            try:
                response = con.edit_config(config=config, target=target, default_operation=operation)
                con.commit()
            except RPCError as e:
                return (e.xml, 400)
            except:
                return ("Internal Server Error", 500)
            if response.ok:
                return (response.xml, 201)
            return ("Internal Server Error", 500)

    def __getData(self, templateName, params):
        env = Environment(
            autoescape=False,
            loader=FileSystemLoader("./templates/"),
            trim_blocks=False,
            undefined=StrictUndefined
        )
        return env.get_template(templateName).render(params)

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