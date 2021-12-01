#!/usr/bin/env python3
from flask import Flask, request, Response, jsonify
from cisco import CiscoNC, CiscoSSH
import json
import argparse

app = Flask(__name__)
dryRun = False

@app.route('/set-dry-run', methods=["POST"])
def setDryRun() -> Response:
    try:
        dryRun = request.json["dryRun"]
        return Response(status=201)
    except:
        return Response(response="Invalid Request", status=400)

@app.route('/<hostname>/interfaces', methods=["GET"])
def getInterfaces(hostname: str) -> Response:
    device = {
        "dryRun": dryRun,
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
        "dryRun": dryRun,
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
        "dryRun": dryRun,
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
        "dryRun": dryRun,
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

    