"""
Firebase extensions module.

Provides the Firestore database client for use across services.
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_KEY_PATH = os.path.join(BASE_DIR, 'firestore_key.json')

# Initialize Firebase if not already done
if not firebase_admin._apps:
    try:
        # Method 1: Use firestore_key.json in the same directory (default)
        if os.path.exists(DEFAULT_KEY_PATH):
            cred = credentials.Certificate(DEFAULT_KEY_PATH)
            firebase_admin.initialize_app(cred)
            print(f"Firebase initialized with: {DEFAULT_KEY_PATH}")
        # Method 2: Use GOOGLE_APPLICATION_CREDENTIALS environment variable
        elif os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print(f"Firebase initialized with: {cred_path}")
        # Method 3: Use service account JSON from environment variable
        elif os.getenv('FIREBASE_SERVICE_ACCOUNT'):
            service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT'))
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized with FIREBASE_SERVICE_ACCOUNT env var")
        # Method 4: Default credentials (for Google Cloud environments)
        else:
            firebase_admin.initialize_app()
            print("Firebase initialized with default credentials")
    except Exception as e:
        print(f"Firebase initialization error: {e}")

# Export the Firestore client
db = firestore.client()
