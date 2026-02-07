"""
User Profile Blueprint.

Handles health and nutrition profile management for users.
"""

from flask import Blueprint, jsonify, request
from services.health_service import (
    post_health_data,
    get_health_data,
    patch_health_data,
    delete_health_data
)
from services.nutrition_service import (
    post_nutrition_data,
    get_nutrition_data,
    update_nutrition_data,
    delete_nutrition_data
)

user_bp = Blueprint('user', __name__, url_prefix='/users')


# ============================================================================
# Health Profile Endpoints
# ============================================================================

@user_bp.route('/<user_id>/health', methods=['POST'])
def create_health_profile(user_id):
    """
    Create initial health data for a user.
    
    Request Body:
        {
            "weight": 75.5,
            "height": 180,
            "age": 28,
            "gender": "male",
            "activity_level": "moderate",
            "health_conditions": ["none"],
            "fitness_goal": "weight_loss"
        }
    
    Returns:
        201: Health profile created
        400: Missing required fields
        404: User not found
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    # Validate required fields
    required_fields = ['weight', 'height', 'age']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing_fields': missing_fields
        }), 400
    
    # Calculate BMI
    try:
        weight = float(data['weight'])
        height = float(data['height'])
        height_m = height / 100
        data['bmi'] = round(weight / (height_m ** 2), 2)
    except (ValueError, ZeroDivisionError):
        return jsonify({'error': 'Invalid weight or height values'}), 400
    
    result, status_code = post_health_data(user_id, data)
    return jsonify(result), status_code


@user_bp.route('/<user_id>/health', methods=['GET'])
def get_health_profile(user_id):
    """
    Retrieve health profile for a user.
    
    Returns:
        200: Health profile data
        404: User not found or health profile doesn't exist
        500: Server error
    """
    result, status_code = get_health_data(user_id)
    return jsonify(result), status_code


@user_bp.route('/<user_id>/health', methods=['PUT'])
def update_health_profile(user_id):
    """
    Update existing health data for a user.
    
    Request Body (all fields optional):
        {
            "weight": 74.0,
            "height": 180,
            "age": 29,
            "activity_level": "active"
        }
    
    Returns:
        200: Health profile updated
        400: No data provided
        404: User not found
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    if not data:
        return jsonify({'error': 'No update data provided'}), 400
    
    # Recalculate BMI if weight or height changed
    if 'weight' in data or 'height' in data:
        # Need to get current values for BMI calculation
        current_result, status = get_health_data(user_id)
        if status == 200:
            current_profile = current_result.get('profile', {})
            weight = float(data.get('weight', current_profile.get('weight', 0)))
            height = float(data.get('height', current_profile.get('height', 1)))
            if height > 0:
                height_m = height / 100
                data['bmi'] = round(weight / (height_m ** 2), 2)
    
    result, status_code = patch_health_data(user_id, data)
    return jsonify(result), status_code


@user_bp.route('/<user_id>/health', methods=['DELETE'])
def remove_health_profile(user_id):
    """
    Remove health data fields from user profile.
    
    Returns:
        200: Health profile deleted
        404: User not found
        500: Server error
    """
    result, status_code = delete_health_data(user_id)
    return jsonify(result), status_code


# ============================================================================
# Nutrition Profile Endpoints
# ============================================================================

@user_bp.route('/<user_id>/nutrition', methods=['POST'])
def create_nutrition_profile(user_id):
    """
    Create nutrition preferences for a user.
    
    Request Body:
        {
            "allergies": ["peanuts", "shellfish"],
            "diet_type": "vegetarian",
            "calorie_goal": 2000,
            "protein_goal": 150,
            "carb_goal": 200,
            "fat_goal": 65,
            "meals_per_day": 4,
            "dietary_restrictions": ["low-sodium"],
            "cuisine_preferences": ["mediterranean", "asian"]
        }
    
    Returns:
        201: Nutrition profile created
        404: User not found
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    # Set defaults
    nutrition_data = {
        'allergies': data.get('allergies', []),
        'diet_type': data.get('diet_type', 'standard'),
        'calorie_goal': data.get('calorie_goal', 2000),
        'protein_goal': data.get('protein_goal'),
        'carb_goal': data.get('carb_goal'),
        'fat_goal': data.get('fat_goal'),
        'meals_per_day': data.get('meals_per_day', 3),
        'dietary_restrictions': data.get('dietary_restrictions', []),
        'cuisine_preferences': data.get('cuisine_preferences', [])
    }
    
    result, status_code = post_nutrition_data(user_id, nutrition_data)
    return jsonify(result), status_code


@user_bp.route('/<user_id>/nutrition', methods=['GET'])
def get_nutrition_profile(user_id):
    """
    Retrieve nutrition profile for a user.
    
    Returns:
        200: Nutrition profile data
        404: User not found or nutrition profile doesn't exist
        500: Server error
    """
    result, status_code = get_nutrition_data(user_id)
    return jsonify(result), status_code


@user_bp.route('/<user_id>/nutrition', methods=['PUT'])
def update_nutrition_profile(user_id):
    """
    Update nutrition preferences for a user.
    
    Request Body (all fields optional):
        {
            "calorie_goal": 1800,
            "diet_type": "keto"
        }
    
    Returns:
        200: Nutrition profile updated
        400: No data provided
        404: User not found
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    if not data:
        return jsonify({'error': 'No update data provided'}), 400
    
    result, status_code = update_nutrition_data(user_id, data)
    return jsonify(result), status_code


@user_bp.route('/<user_id>/nutrition', methods=['DELETE'])
def remove_nutrition_profile(user_id):
    """
    Remove nutrition data from user profile.
    
    Returns:
        200: Nutrition profile deleted
        404: User not found
        500: Server error
    """
    result, status_code = delete_nutrition_data(user_id)
    return jsonify(result), status_code
