import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid

# Use environment variables to configure MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.environ.get("MONGO_DB", "students_db")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION", "students")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
students_collection = db[MONGO_COLLECTION]


def add(student=None):
    # Check if a student with the same first and last name already exists
    existing = students_collection.find_one(
        {"first_name": student.first_name, "last_name": student.last_name}
    )
    if existing:
        return "Student already exists", 409

    # Convert student object to dict and insert into MongoDB
    student_dict = student.to_dict()
    student_dict["student_id"] = str(uuid.uuid4())
    print(student_dict)
    _ = students_collection.insert_one(student_dict)
    # Set the student_id to the MongoDB _id (converted to string)
    return student_dict.get("student_id"), 200


def get_by_id(student_id=None, subject=None):
    try:
        # Look up the student by _id (converted from string to ObjectId)
        student = students_collection.find_one({"student_id": str(student_id)})
    except Exception:
        return {"error": "Invalid student ID."}, 400

    if not student:
        return {"error": "Student not found."}, 404

    # Add the string version of _id to the returned document
    # student["student_id"] = str(student["_id"])
    del student["_id"]
    return student, 200


def delete(student_id=None):
    try:
        print(student_id)
        result = students_collection.delete_one(
            {"student_id": str(student_id)}
        )
    except Exception:
        return {"error": "Invalid student ID."}, 400

    if result.deleted_count == 0:
        return {"error": "Student not found."}, 404

    return {"message": "Student deleted successfully."}, 200
