#!/usr/bin/env python
"""
Author: George Coe
Email: gcoe95@gmail.com

A selection of classes to represent a Cisco device and
provide configuration capabilities via either Netconf or 
SSH based CLI

"""
import os
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from ncclient import manager
from ncclient.operations.rpc import RPCError
from ncclient.xml_ import *
from netmiko import ConnectHandler

class Cisco:
    """
    Cisco

    A base class used to represent a Cisco network device

    Parameters
    ----------
    hostname : str
        The hostname of the cisco device
    username : str
        The username used to connect to the device
    password : str
        The password used to connect to the device
    dryRun : bool
        Determins if requests are executed on device or dummy response returned
    """

    def __init__(self, hostname, username, password, dryRun=False):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.dryRun = dryRun

class CiscoNC(Cisco):
    """
    CiscoNC

    A subclass of Cisco to communicate with a Cisco device using Netconf

    Parameters
    ----------
    port : int
        The TCP port used for the connection
    **kwargs
        The args passed to the Cisco class
    """

    def __init__(self, port, **kwargs):
        super(CiscoNC, self).__init__(**kwargs)
        self.port = port
    
    def getInterfaces(self):
        """
        Get Device Interfaces

        Sends a netconf request to the Cisco device to get everythin under
        the interfaces subtree

        Returns
        ------
        xml : str
            The netconf xml returned from the device
        status_code : int
            The HTTP status code for the server to respond with
        """
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
        """
        Create an Interface

        Creates a loopback interface, using Netconf, based on a jinja2 template and the data
        stored in the params arguement

        Parameters
        ----------
        params : dict
            The parameters used to fill in the jinja2 template

        Retruns
        -------
        xml : str
            The Netconf xml returned from the request
        status_code : int
            The HTTP status code for the server to respond with
        """
        try: body = self.__getData("loopback_create.xml", params)
        except Exception as e: return (str(e), 400)       
        return self.__editConfig(body, "candidate")

    def deleteInterface(self):
        """
        Delete an Interface

        Deletes a loopback interface, using Netconf, based on a jinja2 template

        Retruns
        -------
        xml : str
            The Netconf xml returned from the request
        status_code : int
            The HTTP status code for the server to respond with
        """
        try: body = self.__getData("loopback_delete.xml", {"name": "Loopback66"}) 
        except Exception as e: return (str(e), 400) 
        return self.__editConfig(body, "candidate")

    # Create a netconf connection to the device
    def __createConnection(self):
        """
        Create Connection

        Creates a netconf connection to the device using the ncclint package

        Retruns
        -------
        connection : ncclient.manager
        """
        return manager.connect(
            host=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            hostkey_verify=False,
            device_params={'name':'iosxr'}
        )

    def __editConfig(self, config, target, operation="merge"):
        """
        Edit Config Using Netconf

        sends a Netconf request to edit the configuration of a device and commit it
        to running config. 

        Parameters
        ----------
        config : str
            The Netconf used to configure the device
        target : str
            The target datastore to configure
        operation : str
            The default operation used to apply the configuration (see ncclient docs)

        Retruns
        -------
        xml : str
            The Netconf xml returned from the request
        status_code : int
            The HTTP status code for the server to respond with
        """
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
        """
        Get Data

        Returns a rendered jinja2 template

        Parameters
        ----------
        templateName : str
            The name of the template to render
        params : dict
            The values required to render the template

        Retruns
        -------
        template : str
            The rendered netconf template
        """
        path = os.path.realpath(__file__)  
        path = os.path.dirname(os.path.abspath(path))               
        env = Environment(
            autoescape=False,
            loader=FileSystemLoader(f"{path}/templates/"),
            trim_blocks=False,
            undefined=StrictUndefined
        )
        return env.get_template(templateName).render(params)

class CiscoSSH(Cisco):
    """
    CiscoSSH

    A subclass of Cisco to communicate with a Cisco device using CLI commands over SSH

    Parameters
    ----------
    port : int
        The TCP port used for the connection
    **kwargs
        The args passed to the Cisco class
    """

    def __init__(self, port, **kwargs):
        super(CiscoSSH, self).__init__(**kwargs)
        self.port = port

    def __createConnection(self):
        """
        Create Connection

        Creates an SSH connection to the device using the netmiko package

        Retruns
        -------
        connection : CiscoBaseConnection
            The connection to the Cisco device (See Netmiko docs)
        """
        device = {
            'device_type': 'cisco_xr',
            'host': self.hostname,
            'username': self.username,
            'password': self.password,
            'port': 22,
        }
        return ConnectHandler(**device)

    def getInterfaces(self):
        """
        Get Interfaces

        Returns a json formatted response of the 'sho ip int brief' cli command

        Retruns
        -------
        response : josn
            A json representaion of the command output
        status_code : int
            The HTTP status code for the server to respond with
        """
        commands = [
            "term len 0",
            "show ip int br"
        ]
        if self.dryRun: return (commands, 200)
        with self.__createConnection() as con:            
            for cmd in commands:
                response = con.send_command(cmd) 
        return (self.__responseToJson(response), 200)

    def __responseToJson(self, response):
        """
        Response To Json

        Take the cli output from 'show ip int brief' and formats it into
        a json representation

        Parameters
        ----------
        response : str
            The cli response from the command
        
        Returns
        -------
        jsonRsp : dict
            json representation of the cli command
        """
        responseTrimed = response.split('\n')[2:]
        keys = responseTrimed[0].split()
        interfaces = [line.split() for line in responseTrimed[1:]]
        jsonRsp = []
        for interfaceValues in interfaces:
            jsonRsp.append(dict(zip(keys, interfaceValues)))
        return jsonRsp


