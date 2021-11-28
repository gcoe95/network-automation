from flask import Flask, request, jsonify
from cisco import CiscoNC, CiscoSSH
import json

app = Flask(__name__)

@app.route('/<hostname>/interfaces', methods=["GET"])
def getInterfaces(hostname: str):
    device = {
        "hostname": hostname,
        "username": "admin",
        "password": "C1sco12345",
        "port": 830
    }
    cisco = CiscoNC(**device)
    data = cisco.getInterfaces()
    return (str(data), 200)

@app.route('/<hostname>/interfacescreate', methods=["GET"])
def createInterfaces(hostname: str):
    device = {
        "hostname": hostname,
        "username": "admin",
        "password": "C1sco12345",
        "port": 830
    }
    cisco = CiscoNC(**device)
    data = cisco.createInterface()
    return (str(data), 200)

@app.route('/<hostname>/interfaces/<interface>', methods=["DELETE"])
def deleteInterfaces(hostname:str, interface: str):
    device = {
        "hostname": hostname,
        "username": "admin",
        "password": "C1sco12345",
        "port": 830
    }
    cisco = CiscoNC(**device)
    data = cisco.deleteInterface()
    return (str(data), 200)

@app.route('/ssh/<hostname>/interfaces', methods=["GET"])
def getInterfacesSSH(hostname: str):
    device = {
        "dryRun": False,
        "hostname": hostname,
        "username": "admin",
        "password": "C1sco12345",
        "port": 22
    }
    cisco = CiscoSSH(**device)
    data = cisco.getInterfaces()
    return (str(data), 200)

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")

    