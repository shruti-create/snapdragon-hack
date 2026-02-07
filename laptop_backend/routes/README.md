# Routes Documentation

## Auth (`auth.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/register` | Register user with `email`, `username`, `password` |
| GET | `/users/<user_id>` | Get user by ID |
| DELETE | `/users/<user_id>` | Delete user and all data |

## Health Profile (`user.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/<user_id>/health` | Create health profile (`weight`, `height`, `age` required) |
| GET | `/users/<user_id>/health` | Get health profile |
| PUT | `/users/<user_id>/health` | Update health profile |
| DELETE | `/users/<user_id>/health` | Remove health profile |

## Nutrition Profile (`user.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/<user_id>/nutrition` | Create nutrition preferences (`allergies`, `diet_type`, `calorie_goal`) |
| GET | `/users/<user_id>/nutrition` | Get nutrition profile |
| PUT | `/users/<user_id>/nutrition` | Update nutrition profile |
| DELETE | `/users/<user_id>/nutrition` | Remove nutrition profile |

## Plans (`plan.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/<user_id>/plan` | Create plan (`plan_type`: diet/workout/combined) |
| GET | `/users/<user_id>/plan` | Get active plan (add `?include_history=true` for all) |
| PUT | `/users/<user_id>/plan` | Update plan status/preferences |
| DELETE | `/users/<user_id>/plan/<plan_id>` | Delete specific plan |

## Tracking (`tracking.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/<user_id>/tracking/meals` | Log meal (`meal_type`: breakfast/lunch/dinner/snacks) |
| POST | `/users/<user_id>/tracking/workout` | Log workout (`completed`, `exercises_completed`, `duration_minutes`) |
| GET | `/users/<user_id>/tracking/daily` | Get daily log (add `?date=YYYY-MM-DD`) |
| GET | `/users/<user_id>/tracking/history` | Get tracking history |
| POST | `/users/<user_id>/tracking/water` | Log water intake (`amount_ml`) |
| POST | `/users/<user_id>/tracking/wellness` | Log wellness (`sleep_hours`, `mood`, `energy_level`) |

## Response Format

All endpoints return JSON with appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad request
- `404` - Not found
- `500` - Server error
