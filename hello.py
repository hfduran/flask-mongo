import asyncio

from flask import Flask
from flask import request
from pymongo import MongoClient

app = Flask(__name__)

uri = "mongodb://127.0.0.1:27017"

client = MongoClient('localhost', 27017)

db = client.flask_db
things = db.things


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.get("/ping")
def ping():
    try:
        print("Pinged")
        return "<p> Pinged </p>"
    except Exception as e:
        print(e)
        return "<p> Not Pinged </p>"


@app.post("/something")
def post_something():
    data = request.get_json()
    something = data["something"]
    things.insert_one({"thing": something})
    return f"Inserted {something}"
