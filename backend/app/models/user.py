from ..db import get_db 
from pymongo import MongoClient
import os
#for encryption
import bcrypt

# Author : av42956 
# MODEL : userModel

db = get_db("Users")
users_collection = db["Users"]

def find_user_by_username(username):
     return users_collection.find_one({"userid": username})

# new functions for encryption
def hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(username, password):
    hashed = hash_password(password).decode('utf-8')
    return users_collection.insert_one({"userid": username, "password": hashed})