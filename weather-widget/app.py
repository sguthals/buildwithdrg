import datetime
from flask import Flask, render_template, request, jsonify, redirect
import json
import requests
import pickle
import os

from get_key import get_key
from config import config
from tools.utils import celsius_to_fahrenheit, date_str_to_date


app = Flask(__name__)


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
    timestamp = res["current"]["weather"]["ts"].split("T")[0]
    date = date_str_to_date(timestamp)
    city = res["city"]
    state = res["state"]
    tempC = res["current"]["weather"]["tp"]
    airQ = res["current"]["pollution"]["aqius"]
    ic = res["current"]["weather"]["ic"]
    icon = config["icon_codes"][ic]
    tempF = celsius_to_fahrenheit(tempC)
    return render_template("index.html", tempF=tempF, airQ=airQ, icon=icon, city=city, state=state, date=date)

if __name__ == "__main__":
    host = config["network"]["host"]
    port = config["network"]["port"]
    app.run(host, port)
