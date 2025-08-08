# db.py
import certifi
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Initialize MongoClient with SSL cert verification
mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

def get_db(db_name: str):
    """
    Returns the database object for the given database name.
    """
    return mongo_client[db_name]
