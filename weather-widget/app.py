import datetime
from flask import Flask, render_template, request, jsonify, redirect
from getpass import getpass
import json
import requests
import pickle
import os

from get_key import get_key
from config import config


app = Flask(__name__)

celsius_to_fahrenheit = lambda x: "{}".format(int((x * 1.8) + 32))
date_str_to_ordinal = lambda s: datetime.date(int(s.split("-")[0]), int(s.split("-")[1]), int(s.split("-")[2])).toordinal()


def needs_update():
    todays_date = datetime.date.today().toordinal()
    with open("data.json", "r") as fh:
        data = json.loads(fh.read())
    prev_date_str = data["data"]["current"]["weather"]["ts"].split("T")[0]
    last_update = date_str_to_ordinal(prev_date_str)
    if last_update < todays_date:
        return True
    else:
        return False

update_status = lambda: needs_update()
    

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
    host = config["network"]["host"]
    port = config["network"]["port"]
    app.run(host, port)
    if needs_update():
        var = getpass("Enter environment variable name: ")
        if not os.environ.get(var):
            print("create environment variable to store secret")
        else:
            url = "http://{}:{}/update/{}".format(host, port, var)
            res = requests.get(url)
            print(res.content)