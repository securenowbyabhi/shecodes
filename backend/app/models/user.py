from ..db import get_db 
from pymongo import MongoClient
import os
import bcrypt


# Author : av42956 
# MODEL : userModel

db = get_db("Users")
users_collection = db["Users"]

def find_user_by_username(username):
     return users_collection.find_one({"userid": username})

# def create_user(username, password):
#     return users_collection.insert_one({"userid": username, "password": password})



def hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)

def create_user(username, password):
    hashed = hash_password(password)
    return users_collection.insert_one({"userid": username, "password": hashed})
