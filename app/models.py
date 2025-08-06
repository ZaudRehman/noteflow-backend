from pymongo import MongoClient 
from datetime import datetime
import bson
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client.noteflow

def get_user_by_email(email: str):
    return db.users.find_one({"email": email})

def get_user_by_id(user_id: str):
    try:
        oid = bson.ObjectId(user_id)
    except Exception:
        return None
    return db.users.find_one({"_id": oid})

def insert_user(user: dict):
    user["created_at"] = datetime.now()
    return db.users.insert_one(user)

def insert_note(note: dict):
    note["created_at"] = datetime.now()
    return db.notes.insert_one(note)

def get_note_by_id(note_id: str):
    try:
        oid = bson.ObjectId(note_id)
    except Exception:
        return None
    return db.notes.find_one({"_id": oid})

def get_notes_by_user_id(user_id: str):
    try:
        oid = bson.ObjectId(user_id)
    except Exception:
        return None
    return db.notes.find({"user_id": oid})

def update_note(note_id: str, update: dict):
    oid = bson.ObjectId(note_id)
    return db.notes.update_one({"_id": oid}, {"$set": update})

def delete_note_by_id(note_id: str):
    oid = bson.ObjectId(note_id)
    return db.notes.delete_one({"_id": oid})

def list_user_notes(user_id: str):
    return list(db.notes.find({"collaborators": user_id}))