from ..db import get_db 
from pymongo import MongoClient
import os


# Author : av42956 
# MODEL : userModel

db = get_db("Users")
users_collection = db["Users"]

def find_user_by_username(username):
     return users_collection.find_one({"userid": username})

def create_user(username, password):
    return users_collection.insert_one({"userid": username, "password": password})
