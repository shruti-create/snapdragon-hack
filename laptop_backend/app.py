import os
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from pymongo import MongoClient, ReturnDocument

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

db_name = os.getenv("MONGO_DB", "snapdragon")
db = client[db_name]
collection = db["health"]

# Exercise dataset collections
exercises_col = db["exercises"]
body_parts_col = db["bodyParts"]
equipments_col = db["equipments"]
muscles_col = db["muscles"]


def serialize_doc(doc):
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "status": doc.get("status"),
        "notes": doc.get("notes"),
    }


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"})


@app.get("/api/health")
def list_health():
    docs = [serialize_doc(doc) for doc in collection.find()]
    return jsonify(docs)


@app.post("/api/health")
def create_health():
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    status = payload.get("status")

    if not name or not status:
        return jsonify({"error": "name and status are required"}), 400

    doc = {
        "name": name,
        "status": status,
        "notes": payload.get("notes"),
    }
    result = collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return jsonify(serialize_doc(doc)), 201


@app.get("/api/health/<string:doc_id>")
def get_health(doc_id):
    try:
        doc = collection.find_one({"_id": ObjectId(doc_id)})
    except Exception:
        return jsonify({"error": "invalid id"}), 400

    if not doc:
        return jsonify({"error": "not found"}), 404

    return jsonify(serialize_doc(doc))


@app.put("/api/health/<string:doc_id>")
def update_health(doc_id):
    payload = request.get_json(silent=True) or {}
    update = {}

    for key in ("name", "status", "notes"):
        if key in payload:
            update[key] = payload[key]

    if not update:
        return jsonify({"error": "no updatable fields provided"}), 400

    try:
        result = collection.find_one_and_update(
            {"_id": ObjectId(doc_id)},
            {"$set": update},
            return_document=ReturnDocument.AFTER,
        )
    except Exception:
        return jsonify({"error": "invalid id"}), 400

    if not result:
        return jsonify({"error": "not found"}), 404

    return jsonify(serialize_doc(result))


@app.delete("/api/health/<string:doc_id>")
def delete_health(doc_id):
    try:
        result = collection.delete_one({"_id": ObjectId(doc_id)})
    except Exception:
        return jsonify({"error": "invalid id"}), 400

    if result.deleted_count == 0:
        return jsonify({"error": "not found"}), 404

    return jsonify({"deleted": True})


# Exercise endpoints
@app.get("/api/exercises")
def list_exercises():
    """List all exercises with optional filtering."""
    # Get query parameters for filtering
    body_part = request.args.get("bodyPart")
    equipment = request.args.get("equipment")
    target_muscle = request.args.get("targetMuscle")
    
    query = {}
    if body_part:
        query["bodyParts"] = body_part
    if equipment:
        query["equipments"] = equipment
    if target_muscle:
        query["targetMuscles"] = target_muscle
    
    exercises = list(exercises_col.find(query, {"_id": 0}))
    return jsonify({"count": len(exercises), "exercises": exercises})


@app.get("/api/exercises/<string:exercise_id>")
def get_exercise(exercise_id):
    """Get a specific exercise by exerciseId."""
    exercise = exercises_col.find_one({"exerciseId": exercise_id}, {"_id": 0})
    
    if not exercise:
        return jsonify({"error": "exercise not found"}), 404
    
    return jsonify(exercise)


@app.get("/api/bodyParts")
def list_body_parts():
    """List all body parts."""
    body_parts = list(body_parts_col.find({}, {"_id": 0}))
    return jsonify({"count": len(body_parts), "bodyParts": body_parts})


@app.get("/api/equipments")
def list_equipments():
    """List all equipments."""
    equipments = list(equipments_col.find({}, {"_id": 0}))
    return jsonify({"count": len(equipments), "equipments": equipments})


@app.get("/api/muscles")
def list_muscles():
    """List all muscles."""
    muscles = list(muscles_col.find({}, {"_id": 0}))
    return jsonify({"count": len(muscles), "muscles": muscles})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
