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
    
    def _parse_request(self):
        """Parse URL and extract parameters"""
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')

        # Extract ID if present
        parts = path.split('/')
        if len(parts) > 2 and parts[1] == 'transactions':
            return parts[1], parts[2] if len(parts) > 2 else None
        elif len(parts) > 1 and parts[1] == 'transactions':
            return parts[1], None
        return None, None

    def _verify_auth(self):
        """Validate Basic Authentication with HARDCODED credentials"""
        auth_header = self.headers.get('Authorization')

        # DEBUG: Print what we receive
        print(f"\n[DEBUG] Auth header received: {auth_header}")

        if not auth_header:
            print("[DEBUG] No Authorization header")
            return False

        try:
            # Check if it starts with 'Basic '
            if not auth_header.startswith('Basic '):
                print(f"[DEBUG] Header doesn't start with 'Basic '")
                return False

            # Extract the base64 part
            encoded = auth_header[6:]  # Remove 'Basic '
            print(f"[DEBUG] Base64 string: {encoded}")

            # Decode base64
            decoded_bytes = base64.b64decode(encoded)
            decoded = decoded_bytes.decode('utf-8')
            print(f"[DEBUG] Decoded string: {decoded}")

            # Split username and password
            if ':' not in decoded:
                print("[DEBUG] No colon in decoded string")
                return False

            user, pwd = decoded.split(':', 1)
            print(f"[DEBUG] Username: '{user}', Password: '{pwd}'")

            # Check against HARDCODED users
            if user not in self.API_USERS:
                print(f"[DEBUG] User '{user}' not in valid users")
                return False

            if self.API_USERS[user] != pwd:
                print(f"[DEBUG] Password mismatch. Expected: '{self.API_USERS[user]}'")
                return False

            print(f"[DEBUG] Authentication SUCCESS for user: {user}")
            return True

        except Exception as e:
            print(f"[DEBUG] Auth error: {str(e)}")
            return False

    def _response(self, status, data=None, message=""):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        resp = {"status": "success" if status < 400 else "error"}
        if message:
            resp["message"] = message
        if data is not None:
            resp["data"] = data

        self.wfile.write(json.dumps(resp).encode())

    def _get_request_body(self):
        """Extract JSON from request body"""
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None

        try:
            body = self.rfile.read(length).decode('utf-8')
            return json.loads(body)
        except:
            return None
