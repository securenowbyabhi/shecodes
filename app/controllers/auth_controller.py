from flask import jsonify, session
from ..models.user import find_user_by_username, create_user
from pymongo import MongoClient
import bcrypt 
import os

# Author : av42956 
# Controller : to manage login and register user

client = MongoClient(os.environ.get("MONGO_URI"))
db = client.hardware_app
users_collection = db.users


def handle_register(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400


    if users_collection.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users_collection.insert_one({
        'username': username,
        'password': hashed_password.decode('utf-8')  
    })

    return jsonify({'message': 'User registered successfully'}), 201

def handle_login(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = find_user_by_username(username)
    if not user or user['password'] != password:
        return jsonify({"message": "Invalid credentials"}), 401

    session['username'] = username
    return jsonify({"message": f"Welcome, {username}!"}), 200
