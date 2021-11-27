from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/<host>/interfaces', methods=["GET"])
def getInterfaces(hostname: str):
    pass





if __name__ == "__main__":
    app.run(port=8080, host="10.101.88.118")

    