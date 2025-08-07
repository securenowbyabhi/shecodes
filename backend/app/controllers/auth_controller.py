from flask import jsonify, session
from ..models.user import find_user_by_username, create_user
#import bcrypt 
from ..db import get_db
from ..models.projects import get_project_by_id, get_hardware_status,create_project
from flask import jsonify, session
from ..models.user import find_user_by_username, create_user, check_password


# Author : av42956 
# Controller : to manage login and register user



# def handle_register(request):
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'Username and password required'}), 400


#     if find_user_by_username(username):
#         return jsonify({'message': 'Username already exists'}), 400

#     #hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#     create_user(username, password)
#     #create_user(username, hashed_password)

#     return jsonify({'message': 'User registered successfully'}), 201
def handle_register(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password required'}), 400

    if find_user_by_username(username):
        return jsonify({'message': 'Username already exists'}), 400

    # Hashing happens inside create_user now
    create_user(username, password)

    return jsonify({'message': 'User registered successfully'}), 201


# def handle_login(request):
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     user = find_user_by_username(username)
#     if not user or user['password'] != password:
#         return jsonify({"message": "Invalid credentials"}), 401

#     session['username'] = username
#     return jsonify({"message": f"Welcome, {username}!"}), 200

def handle_login(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    user = find_user_by_username(username)
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    if not check_password(password, user["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    session['username'] = username  # Optional: for login session management
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


    if get_project_by_id(projectid):
        return jsonify({'message': 'Project Id already exists'}), 400

    

    create_project(projectid, projectname, description)

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

    # Get project
    project = project_db["Projects"].find_one({"projectid": project_id})
    if not project:
        return jsonify({"message": "Project not found"}), 404

    # Ensure phardware is initialized
    phardware = list(map(int, project.get("phardware", [0] * len(HARDWARE_INDEX_MAP))))
    phardware += [0] * (len(HARDWARE_INDEX_MAP) - len(phardware))  # Ensure length = 2

    any_updated = False

    for item in hardware_items:
        hardware_id = item.get("hardwareid")
        quantity = item.get("quantity")

        if not hardware_id or quantity in [None, "", 0, "0"]:
            continue  # Skip empty entries

        if hardware_id not in HARDWARE_INDEX_MAP:
            return jsonify({"message": f"Unsupported hardwareid: {hardware_id}"}), 400

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return jsonify({"message": f"Quantity for {hardware_id} must be a number"}), 400

        if quantity <= 0:
            continue

        index = HARDWARE_INDEX_MAP[hardware_id]
        current_checked_out = phardware[index]

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
            phardware[index] = current_checked_out + quantity
            any_updated = True

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
            any_updated = True

    if not any_updated:
        return jsonify({"message": "No valid hardware items to process."}), 400

    project_db["Projects"].update_one(
        {"projectid": project_id},
        {"$set": {"phardware": phardware}}
    )

    return jsonify({
        "message": f"{action.capitalize()} successful",
        "response": {
            "projectid": project_id,
            "checkedOut": phardware
        }
    }), 200
