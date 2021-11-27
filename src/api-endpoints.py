from flask import Flask, request, jsonify
from cisco import Cisco
import json

app = Flask(__name__)

@app.route('/<hostname>/interfaces', methods=["GET"])
def getInterfaces(hostname: str):
    cisco = Cisco(hostname, "admin", "C1sco12345")
    data = cisco.getInterfaces()
    return (str(data), 200)





if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")

    