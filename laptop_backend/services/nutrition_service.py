from google.cloud import firestore
from app.extensions import db


def post_nutrition_data(user_id, week_data):
    """Append a new meal object to the diet array."""
    try:
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        if not doc.exists:
            return {"error": "User not found"}, 404

        doc_ref.update({"diet": firestore.ArrayUnion([week_data])})
        return {"message": "Meal added successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


def update_nutrition_data(user_id, week_index, updated_meal):
    """Update a specific meal entry in the diet array by index.

    Firestore does not support updating array elements by index directly,
    so we fetch the document, modify the array in memory, and write it back.
    """
    try:
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        if not doc.exists:
            return {"error": "User not found"}, 404

        doc_data = doc.to_dict()
        diet = doc_data.get("diet", [])

        if week_index < 0 or week_index >= len(diet):
            return {"error": "Invalid week index"}, 400

        diet[week_index] = updated_meal
        doc_ref.set({"diet": diet}, merge=True)
        return {"message": "Meal updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


def delete_nutrition_data(user_id, week_data_to_match):
    """Remove a specific diet object from the diet array."""
    try:
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        if not doc.exists:
            return {"error": "User not found"}, 404

        doc_ref.update({"diet": firestore.ArrayRemove([week_data_to_match])})
        return {"message": "Meal removed successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
