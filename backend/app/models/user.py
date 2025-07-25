from ..db import mongo

# Author : av42956 
# MODEL : userModel

def find_user_by_username(username):
    return mongo.db.Users.find_one({"userId": username})

def create_user(username, password):
    return mongo.db.Users.insert_one({"userId": username, "password": password})
