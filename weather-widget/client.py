import os
from getpass import getpass
import datetime
import requests
import json

from config import config
from tools.utils import date_str_to_ordinal

host = config["network"]["host"]
port = config["network"]["port"]



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


if needs_update():
    var = getpass("Enter environment variable name: ")
    if not os.environ.get(var):
        print("create environment variable to store secret")
    else:
        url = "http://{}:{}/update/{}".format(host, port, var)
        res = requests.get(url)
        print(res.content)