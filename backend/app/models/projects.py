# app/models/project.py

from ..db import get_db

def get_project_by_id(projectid):
    db = get_db("Projects")
    return db["Projects"].find_one({"projectid": projectid})

def get_hardware_status(): 
    db = get_db("Inventory")
    hw1 = db["Inventory"].find_one({"hardwareid": "hw1"})
    hw2 = db["Inventory"].find_one({"hardwareid": "hw2"})
    return [hw1, hw2]

def create_project(projectid,projectname,projectdescription):
    db = get_db("Projects")
    return db["Projects"].insert_one({"projectid": projectid, "projectname": projectname,
                                     "projectdescription":projectdescription})
