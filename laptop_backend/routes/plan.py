"""
Plan Management Blueprint.

Handles diet and workout plan creation, updates, and retrieval.
"""

from flask import Blueprint, jsonify, request
from services.plan_service import create_plan, get_plan, update_plan, delete_plan

plan_bp = Blueprint('plan', __name__, url_prefix='/users')


def generate_ai_diet_plan(user_data, plan_preferences):
    """
    TODO: Integrate with AI agent to generate personalized diet plan.
    
    This is a placeholder that would be replaced with actual AI agent call.
    """
    return {
        'meals': [
            {
                'meal_type': 'breakfast',
                'name': 'Oatmeal with Berries',
                'calories': 350,
                'protein': 12,
                'carbs': 60,
                'fat': 8,
                'ingredients': ['oats', 'mixed berries', 'honey', 'almonds'],
                'instructions': 'Cook oats, top with berries and almonds'
            },
            {
                'meal_type': 'lunch',
                'name': 'Grilled Chicken Salad',
                'calories': 450,
                'protein': 35,
                'carbs': 25,
                'fat': 20,
                'ingredients': ['chicken breast', 'mixed greens', 'olive oil', 'vegetables'],
                'instructions': 'Grill chicken, serve over mixed greens'
            },
            {
                'meal_type': 'dinner',
                'name': 'Salmon with Vegetables',
                'calories': 500,
                'protein': 40,
                'carbs': 30,
                'fat': 22,
                'ingredients': ['salmon fillet', 'broccoli', 'brown rice', 'lemon'],
                'instructions': 'Bake salmon, serve with steamed vegetables and rice'
            },
            {
                'meal_type': 'snack',
                'name': 'Greek Yogurt with Nuts',
                'calories': 200,
                'protein': 15,
                'carbs': 15,
                'fat': 10,
                'ingredients': ['greek yogurt', 'walnuts', 'honey'],
                'instructions': 'Mix yogurt with nuts and drizzle honey'
            }
        ],
        'daily_totals': {
            'calories': 1500,
            'protein': 102,
            'carbs': 130,
            'fat': 60
        }
    }


def generate_ai_workout_plan(user_data, plan_preferences):
    """
    TODO: Integrate with AI agent to generate personalized workout plan.
    
    This is a placeholder that would be replaced with actual AI agent call.
    """
    return {
        'weekly_schedule': [
            {
                'day': 'Monday',
                'focus': 'Upper Body',
                'exercises': [
                    {'name': 'Push-ups', 'sets': 3, 'reps': 12, 'rest_seconds': 60},
                    {'name': 'Dumbbell Rows', 'sets': 3, 'reps': 10, 'rest_seconds': 60},
                    {'name': 'Shoulder Press', 'sets': 3, 'reps': 10, 'rest_seconds': 60},
                    {'name': 'Bicep Curls', 'sets': 3, 'reps': 12, 'rest_seconds': 45}
                ],
                'duration_minutes': 45,
                'calories_burn_estimate': 300
            },
            {
                'day': 'Tuesday',
                'focus': 'Lower Body',
                'exercises': [
                    {'name': 'Squats', 'sets': 4, 'reps': 12, 'rest_seconds': 60},
                    {'name': 'Lunges', 'sets': 3, 'reps': 10, 'rest_seconds': 60},
                    {'name': 'Deadlifts', 'sets': 3, 'reps': 8, 'rest_seconds': 90},
                    {'name': 'Calf Raises', 'sets': 3, 'reps': 15, 'rest_seconds': 45}
                ],
                'duration_minutes': 50,
                'calories_burn_estimate': 350
            },
            {
                'day': 'Wednesday',
                'focus': 'Rest/Active Recovery',
                'exercises': [
                    {'name': 'Light Walking', 'duration_minutes': 30},
                    {'name': 'Stretching', 'duration_minutes': 15}
                ],
                'duration_minutes': 45,
                'calories_burn_estimate': 150
            },
            {
                'day': 'Thursday',
                'focus': 'Core & Cardio',
                'exercises': [
                    {'name': 'Planks', 'sets': 3, 'duration_seconds': 45},
                    {'name': 'Mountain Climbers', 'sets': 3, 'reps': 20, 'rest_seconds': 45},
                    {'name': 'Russian Twists', 'sets': 3, 'reps': 20, 'rest_seconds': 45},
                    {'name': 'HIIT Intervals', 'sets': 5, 'duration_seconds': 30, 'rest_seconds': 30}
                ],
                'duration_minutes': 40,
                'calories_burn_estimate': 400
            },
            {
                'day': 'Friday',
                'focus': 'Full Body',
                'exercises': [
                    {'name': 'Burpees', 'sets': 3, 'reps': 10, 'rest_seconds': 60},
                    {'name': 'Pull-ups', 'sets': 3, 'reps': 8, 'rest_seconds': 60},
                    {'name': 'Goblet Squats', 'sets': 3, 'reps': 12, 'rest_seconds': 60},
                    {'name': 'Dips', 'sets': 3, 'reps': 10, 'rest_seconds': 60}
                ],
                'duration_minutes': 50,
                'calories_burn_estimate': 380
            },
            {
                'day': 'Saturday',
                'focus': 'Cardio',
                'exercises': [
                    {'name': 'Running/Jogging', 'duration_minutes': 30},
                    {'name': 'Cycling', 'duration_minutes': 20}
                ],
                'duration_minutes': 50,
                'calories_burn_estimate': 450
            },
            {
                'day': 'Sunday',
                'focus': 'Rest',
                'exercises': [],
                'duration_minutes': 0,
                'calories_burn_estimate': 0
            }
        ],
        'weekly_totals': {
            'total_duration_minutes': 330,
            'total_calories_burn': 2030,
            'workout_days': 6,
            'rest_days': 1
        }
    }


@plan_bp.route('/<user_id>/plan', methods=['POST'])
def create_user_plan(user_id):
    """
    Create a new diet/workout plan for a user.
    
    This endpoint triggers AI agents to generate personalized content.
    
    Request Body:
        {
            "plan_type": "combined",  // "diet", "workout", or "combined"
            "duration_weeks": 4,
            "intensity": "moderate",
            "specific_goals": ["weight_loss", "muscle_gain"],
            "available_equipment": ["dumbbells", "resistance_bands"],
            "workout_days_per_week": 5,
            "notes": "Focus on morning workouts"
        }
    
    Returns:
        201: Plan created successfully
        400: Invalid plan type
        404: User not found
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    # Validate plan type
    plan_type = data.get('plan_type', 'combined')
    if plan_type not in ['diet', 'workout', 'combined']:
        return jsonify({
            'error': 'Invalid plan_type. Must be "diet", "workout", or "combined"'
        }), 400
    
    # Build plan preferences
    plan_preferences = {
        'duration_weeks': data.get('duration_weeks', 4),
        'intensity': data.get('intensity', 'moderate'),
        'specific_goals': data.get('specific_goals', []),
        'available_equipment': data.get('available_equipment', []),
        'workout_days_per_week': data.get('workout_days_per_week', 5),
        'notes': data.get('notes', '')
    }
    
    # Build plan data
    plan_data = {
        'plan_type': plan_type,
        'preferences': plan_preferences,
    }
    
    # TODO: Call AI agents to generate plans
    if plan_type in ['diet', 'combined']:
        plan_data['diet'] = generate_ai_diet_plan({}, plan_preferences)
    
    if plan_type in ['workout', 'combined']:
        plan_data['workouts'] = generate_ai_workout_plan({}, plan_preferences)
    
    result, status_code = create_plan(user_id, plan_data)
    return jsonify(result), status_code


@plan_bp.route('/<user_id>/plan', methods=['GET'])
def get_user_plan(user_id):
    """
    Retrieve the user's current active plan.
    
    Returns:
        200: Plan data
        404: User or plan not found
        500: Server error
    """
    result, status_code = get_plan(user_id)
    return jsonify(result), status_code


@plan_bp.route('/<user_id>/plan', methods=['PUT'])
def update_user_plan(user_id):
    """
    Update an existing plan.
    
    Request Body (all fields optional):
        {
            "status": "paused",
            "diet": [...],
            "workouts": [...]
        }
    
    Returns:
        200: Plan updated successfully
        400: No data provided
        404: User not found
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    if not data:
        return jsonify({'error': 'No update data provided'}), 400
    
    result, status_code = update_plan(user_id, data)
    return jsonify(result), status_code


@plan_bp.route('/<user_id>/plan', methods=['DELETE'])
def delete_user_plan(user_id):
    """
    Delete the user's plan.
    
    Returns:
        200: Plan deleted successfully
        404: User not found
        500: Server error
    """
    result, status_code = delete_plan(user_id)
    return jsonify(result), status_code
