import certifi
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Author : av42956 
# DB : DB Configuration FILE

load_dotenv()

mongo = PyMongo()

def init_db(app: Flask):
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    ca = certifi.where()  # get path to Mozilla's trusted CA bundle
    mongo.init_app(app, tlsCAFile=ca)  # pass CA file explicitly
