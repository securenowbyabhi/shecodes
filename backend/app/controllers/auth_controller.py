from flask import jsonify, session
from ..models.user import find_user_by_username, create_user

# Author : av42956 
# Controller : to manage login and register user

def handle_register(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    if find_user_by_username(username):
        return jsonify({"message": "Username already exists"}), 409

    create_user(username, password)
    return jsonify({"message": "User registered successfully"}), 201

def handle_login(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = find_user_by_username(username)
    if not user or user['password'] != password:
        return jsonify({"message": "Invalid credentials"}), 401

    session['username'] = username
    return jsonify({"message": f"Welcome, {username}!"}), 200
