#!/usr/bin/env python3
from flask import Flask, request, Response, jsonify
from cisco import CiscoNC, CiscoSSH
import json, configparser, os

app = Flask(__name__)

def getConfigFilePath():
    path = os.path.realpath(__file__)  
    path = os.path.dirname(os.path.abspath(path))
    return path+"/config.ini"

def getDryRunState():
    config = configparser.RawConfigParser()
    config.read(getConfigFilePath())
    return config.getboolean("server-setting", "dry_run", fallback=False)

def setDryRunState(state):
    confFile = getConfigFilePath()
    config = configparser.RawConfigParser()
    config.read(confFile)
    config.set("server-setting", "dry_run", str(state))
    config.write(open(confFile, "w")) 

@app.route('/set-dry-run', methods=["POST"])
def setDryRun() -> Response:
    try:
        dryRun = request.json["dryRun"]
        assert(type(dryRun) is bool)
        setDryRunState(dryRun)
        return Response(status=201)
    except Exception as e:
        return Response(response=f"Invalid Request\n{str(e)}\n{getConfigFilePath()}", status=400)

@app.route('/<hostname>/interfaces', methods=["GET"])
def getInterfaces(hostname: str) -> Response:
    device = {
        "dryRun": getDryRunState(),
        "hostname": hostname,
        "username": "admin",
        "password": "C1sco12345",
        "port": 830
    }
    cisco = CiscoNC(**device)
    response = cisco.getInterfaces()
    return Response(response=response[0], status=response[1], mimetype="application/xml")

@app.route('/<hostname>/interfaces/<interface>', methods=["POST"])
def createInterfaces(hostname: str, interface: str) -> Response:
    device = {
        "dryRun": getDryRunState(),
        "hostname": hostname,
        "username": "admin",
        "password": "C1sco12345",
        "port": 830
    }
    cisco = CiscoNC(**device)
    response = cisco.createInterface(request.json)
    return Response(response=response[0], status=response[1], mimetype="application/xml")

@app.route('/<hostname>/interfaces/<interface>', methods=["DELETE"])
def deleteInterfaces(hostname:str, interface: str) -> Response:
    device = {
        "dryRun": getDryRunState(),
        "hostname": hostname,
        "username": "admin",
        "password": "C1sco12345",
        "port": 830
    }
    cisco = CiscoNC(**device)
    response = cisco.deleteInterface()
    return Response(response=response[0], status=response[1], mimetype="application/xml")

@app.route('/ssh/<hostname>/interfaces', methods=["GET"])
def getInterfacesSSH(hostname: str):
    device = {
        "dryRun": getDryRunState(),
        "hostname": hostname,
        "username": "admin",
        "password": "C1sco12345",
        "port": 22
    }
    cisco = CiscoSSH(**device)
    response = cisco.getInterfaces()
    return (jsonify(response[0]), response[1])  

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")

    