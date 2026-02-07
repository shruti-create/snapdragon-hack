"""
Blueprint registration module for the Nutrition & Workout API.
"""

from .auth import auth_bp
from .user import user_bp
from .plan import plan_bp  # Now imports AI-powered plan routes
from .tracking import tracking_bp

__all__ = ['auth_bp', 'user_bp', 'plan_bp', 'tracking_bp']
