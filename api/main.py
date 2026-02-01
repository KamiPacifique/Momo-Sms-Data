"""
Mobile Money Transaction API
Secure REST API with Hardcoded Data
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import base64
from urllib.parse import urlparse
from datetime import datetime


class MomoAPIHandler(BaseHTTPRequestHandler):
    """HTTP Handler for Mobile Money API with Hardcoded Data"""

    # HARDCODED Authentication credentials
    API_USERS = {
        "admin": "admin123",
        "user": "user456",
        "test": "test789"
    }

    # HARDCODED Initial transactions data
    transactions_store = {
        "1001": {
            "id": "1001",
            "amount": 2000.0,
            "transaction_type": "received",
            "sender": "Jane Smith",
            "receiver": "John Doe",
            "timestamp": "2024-05-10T16:30:58",
            "currency": "RWF",
            "status": "completed",
            "reference": "TXN001"
        },
        "1002": {
            "id": "1002",
            "amount": 1000.0,
            "transaction_type": "sent",
            "sender": "John Doe",
            "receiver": "Alice Brown",
            "timestamp": "2024-05-10T17:45:22",
            "currency": "RWF",
            "status": "completed",
            "reference": "TXN002"
        },
        "1003": {
            "id": "1003",
            "amount": 5000.0,
            "transaction_type": "deposit",
            "sender": "Bank",
            "receiver": "John Doe",
            "timestamp": "2024-05-11T09:15:33",
            "currency": "RWF",
            "status": "completed",
            "reference": "TXN003"
        }
    }

    next_id = 1004  # Next available ID
