"""
Authentication & User Management Blueprint.

Handles user registration and basic user operations.
"""

from flask import Blueprint, jsonify, request
from services.user_service import register_user_entry, get_user, delete_user

auth_bp = Blueprint('auth', __name__, url_prefix='/users')


@auth_bp.route('/register', methods=['POST'])
def register_user():
    """
    Create a new user with email, username, and password.
    
    Request Body:
        {
            "email": "user@example.com",
            "username": "johndoe",
            "password": "securepassword123"
        }
    
    Returns:
        201: User created successfully
        400: Missing required fields
        409: Email or username already exists
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    # Validate required fields
    required_fields = ['email', 'username', 'password']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400
    
    email = data['email'].strip().lower()
    username = data['username'].strip()
    password = data['password']
    
    result, status_code = register_user_entry(email, username, password)
    return jsonify(result), status_code


@auth_bp.route('/<user_id>', methods=['GET'])
def get_user_route(user_id):
    """
    Retrieve user information by user ID.
    
    Args:
        user_id: The unique identifier of the user
        
    Returns:
        200: User data
        404: User not found
        500: Server error
    """
    result, status_code = get_user(user_id)
    return jsonify(result), status_code


@auth_bp.route('/<user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    """
    Delete a user account and all associated data.
    
    Args:
        user_id: The unique identifier of the user
        
    Returns:
        200: User deleted successfully
        404: User not found
        500: Server error
    """
    result, status_code = delete_user(user_id)
    return jsonify(result), status_code
