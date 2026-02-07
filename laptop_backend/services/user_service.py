from app.extensions import db


def register_user_entry(email, username, password):
    """Create a new user document with basic credentials."""
    try:
        users_ref = db.collection("users")

        # Check for existing user with the same email
        existing = users_ref.where("email", "==", email).limit(1).get()
        if len(list(existing)) > 0:
            return {"error": "A user with this email already exists"}, 409

        doc_ref = users_ref.document()
        doc_ref.set({
            "email": email,
            "username": username,
            "password": password,
        })
        return {"message": "User registered successfully", "userId": doc_ref.id}, 201
    except Exception as e:
        return {"error": str(e)}, 500
