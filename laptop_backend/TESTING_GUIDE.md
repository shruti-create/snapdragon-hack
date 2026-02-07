# Testing Guide: AI-Powered Plan Management Implementation

## Overview
This guide provides test cases for verifying the new AI-powered plan management routes.

---

## Phase 1: Verify AI Route Swap ✅

### Test: Existing Plan Generation Route
```bash
# Start the backend
python app.py

# Test plan generation (should use AI now, not mock)
curl -X POST http://localhost:5000/users/test123/plan \
  -H "Content-Type: application/json" \
  -d '{
    "plan_type": "diet",
    "duration_weeks": 2,
    "intensity": "moderate"
  }'

# Expected Response:
# - Status 201
# - "message": "Plan created successfully"
# - "ai_generated": true
# - "generation_method": "npu_llm"
# - diet array with AI-generated meals (NOT "Oatmeal with Berries")
```

### Test: Verify Mock Routes Still Available
```bash
# Mock routes should be in routes/plan_mock.py as backup
ls -la routes/plan_mock.py  # Should exist
```

---

## Phase 2: Test Service Helper Functions

### Test: Update Week Workouts
```python
# Direct database test
from services.plan_service import update_week_workouts

new_exercises = [
    {"workoutId": "w1", "name": "Modified Push-ups", "sets": 4, "reps": 15, "completed": False},
    {"workoutId": "w2", "name": "Modified Squats", "sets": 3, "reps": 10, "completed": False}
]

result, status = update_week_workouts("test123", "Week 1", new_exercises)

# Expected:
# status = 200
# result['message'] contains "Workouts for Week 1 updated successfully"
```

### Test: Update Week Meals
```python
# Direct database test
from services.plan_service import update_week_meals

new_meals = {
    "breakfast": {"name": "Modified Breakfast", "calories": 400, "completed": False},
    "lunch": {"name": "Modified Lunch", "calories": 550, "completed": False},
    "dinner": {"name": "Modified Dinner", "calories": 450, "completed": False},
    "snack": {"name": "Modified Snack", "calories": 150, "completed": False}
}

result, status = update_week_meals("test123", "Week 1", new_meals)

# Expected:
# status = 200
# result['message'] contains "Meals for Week 1 updated successfully"
```

---

## Phase 4: Test Adjustment Routes

### Test 1: Workout Adjustment Route
```bash
# Prerequisites:
# 1. User test123 must exist
# 2. User must have active plan with Week 1 workouts

curl -X PUT http://localhost:5000/users/test123/plan/workout/adjust \
  -H "Content-Type: application/json" \
  -d '{
    "week_name": "Week 1",
    "skipped_workouts": ["w1", "w3"],
    "reason": "Knee pain - need low impact"
  }'

# Expected Response (Status 200):
# {
#   "message": "Workout plan adjusted for Week 1",
#   "week": "Week 1",
#   "adjusted_count": 2,
#   "adjusted_exercises": [...]
# }
```

### Test 2: Nutrition Adjustment Route
```bash
# Prerequisites:
# 1. User test123 must exist
# 2. User must have active plan with Week 1 meals

curl -X PUT http://localhost:5000/users/test123/plan/nutrition/adjust \
  -H "Content-Type: application/json" \
  -d '{
    "week_name": "Week 1",
    "extra_calories": 500,
    "day_of_week": 2,
    "notes": "Had extra snacks"
  }'

# Expected Response (Status 200):
# {
#   "message": "Nutrition plan adjusted for Week 1",
#   "week": "Week 1",
#   "calorie_adjustment": -500,
#   "adjusted_meals": {...}
# }
```

### Test 3: Error Handling - Missing Required Field
```bash
# Test missing week_name
curl -X PUT http://localhost:5000/users/test123/plan/workout/adjust \
  -H "Content-Type: application/json" \
  -d '{"skipped_workouts": ["w1"]}'

# Expected: Status 400, error message about week_name
```

### Test 4: Error Handling - Invalid Week
```bash
# Test week that doesn't exist
curl -X PUT http://localhost:5000/users/test123/plan/workout/adjust \
  -H "Content-Type: application/json" \
  -d '{
    "week_name": "Week 99",
    "skipped_workouts": ["w1"]
  }'

# Expected: Status 404, "Week 99 not found"
```

---

## Logging Verification

### Check AI Inference Logs
```bash
# Monitor AI inference logs
tail -f logs/ai_inference.log | grep "AI_INFERENCE"

# Should see messages like:
# AI_INFERENCE: Starting workout adjustment for userId=test123, week=Week 1, skipped=2
# AI_INFERENCE: Workout adjustment completed for userId=test123, week=Week 1, elapsed_time=2.34s
```

### Check Database Logs
```bash
# Monitor database operation logs
tail -f logs/database.log | grep "DB_WRITE"

# Should see messages like:
# DB_WRITE: Updating workouts for userId=test123, week=Week 1
# DB_WRITE: Workouts updated successfully for userId=test123, week=Week 1
```

---

## Integration Test: Full Workflow

### Scenario: User Skips Workouts and Eats Extra Calories

```bash
# 1. Create a plan
curl -X POST http://localhost:5000/users/integration_test/plan \
  -H "Content-Type: application/json" \
  -d '{"plan_type": "combined", "duration_weeks": 2}'

# 2. User skips workouts
curl -X PUT http://localhost:5000/users/integration_test/plan/workout/adjust \
  -H "Content-Type: application/json" \
  -d '{
    "week_name": "Week 1",
    "skipped_workouts": ["w2"],
    "reason": "Back pain"
  }'

# 3. User eats extra calories on day 3
curl -X PUT http://localhost:5000/users/integration_test/plan/nutrition/adjust \
  -H "Content-Type: application/json" \
  -d '{
    "week_name": "Week 1",
    "extra_calories": 300,
    "day_of_week": 3,
    "notes": "Birthday party"
  }'

# 4. Verify plan was updated correctly
curl -X GET http://localhost:5000/users/integration_test/plan
```

---

## Success Criteria Checklist

- [ ] AI routes accessible without `/ai/` prefix
- [ ] Plan generation uses AI, not mock data
- [ ] Mock routes preserved in `plan_mock.py`
- [ ] `POST /users/{id}/plan` works for diet/workout/combined
- [ ] `PUT /users/{id}/plan/workout/adjust` adjusts current week exercises only
- [ ] `PUT /users/{id}/plan/nutrition/adjust` adjusts current week calories only
- [ ] Other weeks remain unchanged after adjustments
- [ ] All operations save to Firestore correctly
- [ ] Comprehensive logging via `ai_logger` and `db_logger`
- [ ] User CRUD routes (auth.py, user.py) remain unchanged
- [ ] Error handling for missing fields, invalid weeks, no plans
