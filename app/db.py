# db.py
import certifi
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

mongo = PyMongo()
mongo_client = MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())


def init_db(app: Flask):
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)

def get_db(db_name: str):
    return mongo_client[db_name]
