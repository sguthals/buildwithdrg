from flask import Flask

app = Flask(__name__, static_folder="static")



if __name__ == "__main__":
    app.run("127.0.0.1", 43123)