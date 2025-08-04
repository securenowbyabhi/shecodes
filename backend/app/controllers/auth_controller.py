from flask import jsonify, session
from ..models.user import find_user_by_username, create_user
from pymongo import MongoClient
import bcrypt 
import os
from ..db import get_db
from ..models.projects import get_project_by_id, get_hardware_status,create_project


# Author : av42956 
# Controller : to manage login and register user

db = get_db("Users")
users_collection = db["Users"]
db = get_db("Projects")
project_collection = db["Projects"]


def handle_register(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400


    if users_collection.find_one({'userid': username}):
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    users_collection.insert_one({
        'userid': username,
        #'password': hashed_password.decode('utf-8')   # Commented for local
        'password': password
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


def handle_project_status(request):
    project_id = request.args.get("projectid")

    if not project_id:
        return jsonify({"message": "projectid is required"}), 400

    project = get_project_by_id(project_id)
    if not project:
        return jsonify({"message": "Project not found"}), 404

    inventory = get_hardware_status()

    response = {
        "projectid": project_id,
        "checkedOut": project.get("phardware", [0, 0]),
        "inventory": [
            {
                "hardwareid": hw["hardwareid"],
                "capacity": hw["capacity"],
                "available": hw["availability"]
            } for hw in inventory
        ]
    }
    return jsonify(response), 200



def handle_create_project(request):
    data = request.get_json()
    projectid = data.get('projectid')
    projectname = data.get('projectname')
    description = data.get('description')
    

    if not projectid or not projectname or not description:
        return jsonify({'message': 'Project Id, Project Name and Description are required'}), 400


    if project_collection.find_one({'projectid': projectid}):
        return jsonify({'message': 'Project Id already exists'}), 400

    

    project_collection.insert_one({
        'projectid': projectid,
        'projectname': projectname,
        'description':description
    })

    return jsonify({'message': 'Project created successfully'}), 200