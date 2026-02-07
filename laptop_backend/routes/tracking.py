"""
Daily Tracking Blueprint.

Handles daily meal and workout tracking for users.
"""

from datetime import date
from flask import Blueprint, jsonify, request
from services.tracking_service import (
    update_meal_completion,
    toggle_workout_status,
    log_daily_meal,
    log_daily_workout
)

tracking_bp = Blueprint('tracking', __name__, url_prefix='/users')


def get_today_date_str():
    """Get today's date as a string in YYYY-MM-DD format."""
    return date.today().strftime('%Y-%m-%d')


@tracking_bp.route('/<user_id>/tracking/meals', methods=['POST'])
def update_meals(user_id):
    """
    Update the meals eaten for the current day.
    
    Request Body:
        {
            "date": "2024-01-15",  // Optional, defaults to today
            "meal_type": "breakfast",  // "breakfast", "lunch", "dinner", "snacks"
            "items": [
                {
                    "name": "Oatmeal",
                    "calories": 300,
                    "protein": 10,
                    "carbs": 50,
                    "fat": 6
                }
            ],
            "notes": "Ate at 8am"
        }
    
    Alternative for plan-based tracking:
        {
            "week_name": "Week 1",
            "meal_type": "breakfast",
            "actual_meal": "Had oatmeal instead of eggs"
        }
    
    Returns:
        200: Meal updated successfully
        400: Invalid data
        404: User not found
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    # Validate meal type
    meal_type = data.get('meal_type')
    valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snacks']
    
    if not meal_type or meal_type not in valid_meal_types:
        return jsonify({
            'error': f'Invalid meal_type. Must be one of: {", ".join(valid_meal_types)}'
        }), 400
    
    # Check if this is plan-based tracking or daily logging
    week_name = data.get('week_name')
    
    if week_name:
        # Plan-based meal completion tracking
        actual_meal = data.get('actual_meal', '')
        result, status_code = update_meal_completion(user_id, week_name, meal_type, actual_meal)
    else:
        # Daily meal logging
        log_date = data.get('date', get_today_date_str())
        items = data.get('items', [])
        result, status_code = log_daily_meal(user_id, log_date, meal_type, items)
    
    return jsonify(result), status_code


@tracking_bp.route('/<user_id>/tracking/workout', methods=['POST'])
def update_workout(user_id):
    """
    Update the workout status for the current day.
    
    Request Body:
        {
            "date": "2024-01-15",  // Optional, defaults to today
            "completed": true,
            "exercises": [
                {
                    "name": "Push-ups",
                    "sets_completed": 3,
                    "reps_completed": 12
                }
            ],
            "duration_minutes": 45,
            "notes": "Felt great today!"
        }
    
    Alternative for plan-based tracking:
        {
            "week_name": "Week 1",
            "workout_id": "workout_123",
            "completed": true
        }
    
    Returns:
        200: Workout updated successfully
        400: Invalid data
        404: User not found
        500: Server error
    """
    data = request.get_json(silent=True) or {}
    
    # Check if this is plan-based tracking or daily logging
    week_name = data.get('week_name')
    workout_id = data.get('workout_id')
    
    if week_name and workout_id:
        # Plan-based workout tracking
        is_completed = data.get('completed', True)
        result, status_code = toggle_workout_status(user_id, week_name, workout_id, is_completed)
    else:
        # Daily workout logging
        log_date = data.get('date', get_today_date_str())
        workout_data = {
            'completed': data.get('completed', True),
            'exercises': data.get('exercises', []),
            'duration_minutes': data.get('duration_minutes', 0),
            'notes': data.get('notes', '')
        }
        result, status_code = log_daily_workout(user_id, log_date, workout_data)
    
    return jsonify(result), status_code


@tracking_bp.route('/<user_id>/tracking/daily', methods=['GET'])
def get_daily_log(user_id):
    """
    Get the daily log for a specific date.
    
    Query Parameters:
        date: Date string (YYYY-MM-DD), defaults to today
    
    Returns:
        200: Daily log data
        404: User not found or no log for date
        500: Server error
    """
    from extensions import db
    
    log_date = request.args.get('date', get_today_date_str())
    
    try:
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'User not found'}), 404
        
        doc_data = doc.to_dict()
        daily_logs = doc_data.get("dailyLogs", {})
        
        if log_date not in daily_logs:
            return jsonify({'error': f'No log found for date: {log_date}'}), 404
        
        return jsonify({'daily_log': daily_logs[log_date], 'date': log_date}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tracking_bp.route('/<user_id>/tracking/history', methods=['GET'])
def get_tracking_history(user_id):
    """
    Get tracking history.
    
    Query Parameters:
        limit: Maximum number of records, defaults to 30
    
    Returns:
        200: List of daily logs
        404: User not found
        500: Server error
    """
    from extensions import db
    
    limit = min(int(request.args.get('limit', 30)), 100)
    
    try:
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'User not found'}), 404
        
        doc_data = doc.to_dict()
        daily_logs = doc_data.get("dailyLogs", {})
        
        # Sort by date descending and limit
        sorted_dates = sorted(daily_logs.keys(), reverse=True)[:limit]
        logs = [{'date': d, **daily_logs[d]} for d in sorted_dates]
        
        return jsonify({'daily_logs': logs, 'total': len(logs)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tracking_bp.route('/<user_id>/tracking/water', methods=['POST'])
def update_water_intake(user_id):
    """
    Update water intake for the day.
    
    Request Body:
        {
            "date": "2024-01-15",  // Optional, defaults to today
            "amount_ml": 250,
            "set_total": false  // If true, set total instead of adding
        }
    
    Returns:
        200: Water intake updated
        400: Invalid data
        404: User not found
        500: Server error
    """
    from extensions import db
    
    data = request.get_json(silent=True) or {}
    
    amount_ml = data.get('amount_ml')
    if amount_ml is None:
        return jsonify({'error': 'amount_ml is required'}), 400
    
    try:
        amount_ml = int(amount_ml)
        log_date = data.get('date', get_today_date_str())
        set_total = data.get('set_total', False)
        
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'User not found'}), 404
        
        doc_data = doc.to_dict()
        daily_logs = doc_data.get("dailyLogs", {})
        
        if log_date not in daily_logs:
            daily_logs[log_date] = {"meals": {}, "workout": None, "water_ml": 0}
        
        if set_total:
            daily_logs[log_date]["water_ml"] = amount_ml
        else:
            daily_logs[log_date]["water_ml"] = daily_logs[log_date].get("water_ml", 0) + amount_ml
        
        doc_ref.set({"dailyLogs": daily_logs}, merge=True)
        
        return jsonify({
            'message': 'Water intake updated',
            'water_intake_ml': daily_logs[log_date]["water_ml"]
        }), 200
    except ValueError:
        return jsonify({'error': 'Invalid amount_ml value'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tracking_bp.route('/<user_id>/tracking/wellness', methods=['POST'])
def update_wellness(user_id):
    """
    Update wellness metrics (sleep, mood, energy) for the day.
    
    Request Body:
        {
            "date": "2024-01-15",  // Optional, defaults to today
            "sleep_hours": 7.5,
            "mood": "good",  // "great", "good", "okay", "bad", "terrible"
            "energy_level": 4  // 1-5 scale
        }
    
    Returns:
        200: Wellness metrics updated
        400: Invalid data
        404: User not found
        500: Server error
    """
    from extensions import db
    
    data = request.get_json(silent=True) or {}
    log_date = data.get('date', get_today_date_str())
    
    try:
        doc_ref = db.collection("users").document(user_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return jsonify({'error': 'User not found'}), 404
        
        doc_data = doc.to_dict()
        daily_logs = doc_data.get("dailyLogs", {})
        
        if log_date not in daily_logs:
            daily_logs[log_date] = {"meals": {}, "workout": None}
        
        wellness = daily_logs[log_date].get("wellness", {})
        
        if 'sleep_hours' in data:
            wellness['sleep_hours'] = float(data['sleep_hours'])
        
        if 'mood' in data:
            valid_moods = ['great', 'good', 'okay', 'bad', 'terrible']
            if data['mood'] not in valid_moods:
                return jsonify({
                    'error': f'Invalid mood. Must be one of: {", ".join(valid_moods)}'
                }), 400
            wellness['mood'] = data['mood']
        
        if 'energy_level' in data:
            energy = int(data['energy_level'])
            if energy < 1 or energy > 5:
                return jsonify({'error': 'energy_level must be between 1 and 5'}), 400
            wellness['energy_level'] = energy
        
        daily_logs[log_date]["wellness"] = wellness
        doc_ref.set({"dailyLogs": daily_logs}, merge=True)
        
        return jsonify({
            'message': 'Wellness metrics updated',
            'wellness': wellness
        }), 200
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
