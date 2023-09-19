# test comment
# second test comment
import os

from bson import json_util
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

uri = os.environ.get("CONN_STR")

print(uri)
# uri = f"mongodb+srv://uspolis:{mongo_password}@cluster0.melr7t2.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, 27017)

db = client.flask_db
things = db.things
students_collection = db.students


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.post("/something")
def post_something():
    data = request.get_json()
    something = data["something"]
    things.insert_one({"thing": something})
    return f"Inserted {something}"


@app.post("/students")
def create_student():
    student_data = request.json
    if student_data:
        result = students_collection.insert_one(student_data)
        return {
            "message": "Student created successfully",
            "student_id": str(result.inserted_id),
        }, 201
    else:
        return {"error": "Invalid data"}, 400


@app.get("/students")
def get_students():
    students = list(students_collection.find({}))
    return json_util.dumps(students)


@app.get("/students/<string:student_id>")
def get_student(student_id):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if student:
        return json_util.dumps(student)
    else:
        return {"error": "Student not found"}, 404


@app.put("/students/<string:student_id>")
def update_student(student_id):
    student_data = request.json
    if student_data:
        result = students_collection.update_one(
            {"_id": ObjectId(student_id)}, {"$set": student_data}
        )
        if result.modified_count > 0:
            return {"message": "Student updated successfully"}
        else:
            return {"error": "Student not found"}, 404
    else:
        return {"error": "Invalid data"}, 400


@app.delete("/students/<string:student_id>")
def delete_student(student_id):
    result = students_collection.delete_one({"_id": student_id})
    if result.deleted_count > 0:
        return {"message": "Student deleted successfully"}
    else:
        return {"error": "Student not found"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
