from app.extensions import db


def create_plan(user_id, plan_data):
    """Initialize the diet and workouts arrays on a user document."""
    try:
        doc_ref = db.collection("users").document(user_id)
        doc_ref.set({
            "diet": plan_data.get("diet", []),
            "workouts": plan_data.get("workouts", []),
        }, merge=True)
        return {"message": "Plan created successfully"}, 201
    except Exception as e:
        return {"error": str(e)}, 500


def get_plan(user_id):
    """Retrieve the diet and workouts from a user document."""
    try:
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        if not doc.exists:
            return {"error": "User not found"}, 404

        doc_data = doc.to_dict()
        return {
            "diet": doc_data.get("diet", []),
            "workouts": doc_data.get("workouts", []),
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500
