from flask import Flask, render_template, request, jsonify, redirect
import json
import requests
import pickle
import os

from get_key import get_key


app = Flask(__name__)

celsius_to_fahrenheit = lambda x: "{}".format(int((x * 1.8) + 32))

@app.route("/update/<val>")
def get_data(val):
    key = get_key(val)
    res = requests.get(f"http://api.airvisual.com/v2/nearest_city?key={key}").json()
    with open("data.json", "w") as fh:
        fh.write(json.dumps(res))
    return "success", 200


@app.route("/index")
def get_local_tempF():
    if not os.path.exists("data.json"):
        return "update data", 500
    with open("data.json", "r") as fh:
        res = json.loads(fh.read())
    res = res["data"]
    #timestamp = res["current"]["weather"]["ts"]
    tempC = res["current"]["weather"]["tp"]
    airQ = res["current"]["pollution"]["aqius"]
    ic = res["current"]["weather"]["ic"]
    tempF = celsius_to_fahrenheit(tempC)
    return render_template("index.html", tempF=tempF, airQ=airQ, ic=ic)

if __name__ == "__main__":
    app.run("127.0.0.1", 43123)