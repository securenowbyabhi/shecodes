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
    return jsonify({"message": "Project data fetched successfully.", "response":response}), 200

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

HARDWARE_INDEX_MAP = {
    "hw1": 0,
    "hw2": 1
}

def handle_checkin_checkout(request):
    data = request.get_json()
    project_id = data.get("projectid")
    action = data.get("action")
    hardware_items = data.get("inventory", [])

    if not all([project_id, action, hardware_items]):
        return jsonify({"message": "projectid, action, and inventory are required"}), 400

    if action not in ["checkin", "checkout"]:
        return jsonify({"message": "Invalid action. Must be 'checkin' or 'checkout'."}), 400

    project_db = get_db("Projects")
    inventory_db = get_db("Inventory")

    project = project_db["Projects"].find_one({"projectid": project_id})
    if not project:
        return jsonify({"message": "Project not found"}), 404

    #phardware = project.get("phardware", ["0"] * len(HARDWARE_INDEX_MAP))
    phardware = list(map(int, project.get("phardware", [0] * len(HARDWARE_INDEX_MAP))))
    if len(phardware) < len(HARDWARE_INDEX_MAP):
        phardware += ["0"] * (len(HARDWARE_INDEX_MAP) - len(phardware))

    for item in hardware_items:
        hardware_id = item.get("hardwareid")
        quantity = item.get("quantity")

        if not hardware_id or quantity is None:
            return jsonify({"message": "Each hardware item must include hardwareid and quantity"}), 400

        if hardware_id not in HARDWARE_INDEX_MAP:
            return jsonify({"message": f"Unsupported hardwareid: {hardware_id}"}), 400

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return jsonify({"message": f"Quantity for {hardware_id} must be a number"}), 400

        if quantity <= 0:
            return jsonify({"message": f"Quantity for {hardware_id} must be greater than 0"}), 400

        index = HARDWARE_INDEX_MAP[hardware_id]
        current_checked_out = int(phardware[index])

        hardware = inventory_db["Inventory"].find_one({"hardwareid": hardware_id})
        if not hardware:
            return jsonify({"message": f"Hardware {hardware_id} not found"}), 404

        if action == "checkout":
            available = hardware["availability"]
            if quantity > available:
                return jsonify({
                    "message": f"Only {available} units of {hardware_id} are available for checkout"
                }), 400

            inventory_db["Inventory"].update_one(
                {"hardwareid": hardware_id},
                {"$inc": {"availability": -quantity}}
            )

            phardware[index] = (current_checked_out + quantity)

        elif action == "checkin":
            if quantity > current_checked_out:
                return jsonify({
                    "message": f"Project has only {current_checked_out} units of {hardware_id} to check in"
                }), 400

            inventory_db["Inventory"].update_one(
                {"hardwareid": hardware_id},
                {"$inc": {"availability": quantity}}
            )

            phardware[index] = current_checked_out - quantity

    project_db["Projects"].update_one(
        {"projectid": project_id},
        {"$set": {"phardware": phardware}}
    )

    inventory = get_hardware_status()

    response = {
        "projectid": project_id,
        "checkedOut": phardware,
        "inventory": [
            {
                "hardwareid": hw["hardwareid"],
                "capacity": hw["capacity"],
                "available": hw["availability"]
            } for hw in inventory if hw
        ]
    }

    return jsonify({
        "message": f"{action.capitalize()} successful",
        "response": response
    }), 200