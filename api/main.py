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
        def do_GET(self):
        """Handle GET requests"""
        # Authentication check
        if not self._verify_auth():
            self._response(401, message="Authentication failed")
            return

        resource, item_id = self._parse_request()

        if resource == 'transactions':
            if item_id:
                # GET single transaction
                if item_id in self.transactions_store:
                    self._response(200, self.transactions_store[item_id])
                else:
                    self._response(404, message="Transaction not found")
            else:
                # GET all transactions
                all_tx = list(self.transactions_store.values())
                self._response(200, {
                    "count": len(all_tx),
                    "transactions": all_tx
                })
        else:
            self._response(404, message="Endpoint not found")

    def do_POST(self):
        """Handle POST requests - Create new transaction"""
        if not self._verify_auth():
            self._response(401, message="Authentication failed")
            return

        resource, _ = self._parse_request()

        if resource == 'transactions':
            data = self._get_request_body()
            if not data:
                self._response(400, message="Invalid JSON data")
                return

            # Validate required fields
            required = ['amount', 'transaction_type', 'sender', 'receiver']
            for field in required:
                if field not in data or not str(data[field]).strip():
                    self._response(400, message=f"Missing field: {field}")
                    return

            try:
                amount = float(data['amount'])
            except:
                self._response(400, message="Invalid amount format")
                return

            # Create transaction with HARDCODED ID generation
            tx_id = str(self.next_id)
            self.next_id += 1

            transaction = {
                "id": tx_id,
                "amount": amount,
                "transaction_type": data['transaction_type'],
                "sender": data['sender'],
                "receiver": data['receiver'],
                "timestamp": data.get('timestamp', datetime.now().isoformat()),
                "currency": data.get('currency', 'RWF'),
                "status": data.get('status', 'pending'),
                "reference": data.get('reference', f"TXN{tx_id}")
            }

            # Store transaction
            self.transactions_store[tx_id] = transaction

            self._response(201, transaction, "Transaction created")
        else:
            self._response(404, message="Endpoint not found")

    def do_PUT(self):
        """Handle PUT requests - Update transaction"""
        if not self._verify_auth():
            self._response(401, message="Authentication failed")
            return

        resource, item_id = self._parse_request()

        if resource == 'transactions' and item_id:
            if item_id not in self.transactions_store:
                self._response(404, message="Transaction not found")
                return

            data = self._get_request_body()
            if not data:
                self._response(400, message="Invalid JSON data")
                return

            # Update transaction
            current = self.transactions_store[item_id]
            updatable = ['amount', 'transaction_type', 'sender', 'receiver',
                         'currency', 'status', 'timestamp']

            for field in updatable:
                if field in data:
                    if field == 'amount':
                        try:
                            current[field] = float(data[field])
                        except:
                            pass
                    else:
                        current[field] = data[field]

            self._response(200, current, "Transaction updated")
        else:
            self._response(404, message="Endpoint not found")

    def do_DELETE(self):
        """Handle DELETE requests"""
        if not self._verify_auth():
            self._response(401, message="Authentication failed")
            return

        resource, item_id = self._parse_request()

        if resource == 'transactions' and item_id:
            if item_id in self.transactions_store:
                del self.transactions_store[item_id]
                self._response(200, message="Transaction deleted")
            else:
                self._response(404, message="Transaction not found")
        else:
            self._response(404, message="Endpoint not found")

def start_server(port=8000):
    """Start the API server with HARDCODED data"""
    server = HTTPServer(('', port), MomoAPIHandler)

    print("\n" + "=" * 60)
    print("MOBILE MONEY TRANSACTION API")
    print("=" * 60)
    print(f"Server: http://localhost:{port}")
    print(f"Transactions: {len(MomoAPIHandler.transactions_store)}")
    print("\nENDPOINTS:")
    print("  GET    /transactions         - List all transactions")
    print("  GET    /transactions/{id}    - Get specific transaction")
    print("  POST   /transactions         - Create new transaction")
    print("  PUT    /transactions/{id}    - Update transaction")
    print("  DELETE /transactions/{id}    - Delete transaction")
    print("\nAUTHENTICATION (Basic Auth):")

    # Show the EXACT base64 strings to use
    print("\nUse these EXACT Authorization headers:")
    print("-" * 50)

    users = MomoAPIHandler.API_USERS
    for username, password in users.items():
        auth_string = f"{username}:{password}"
        encoded = base64.b64encode(auth_string.encode()).decode()
        print(f"\nUsername: {username}")
        print(f"Password: {password}")
        print(f"Full Header: Authorization: Basic {encoded}")
        print(f"cURL Command:")
        print(f'  curl -X GET "http://localhost:{port}/transactions" \\')
        print(f'    -H "Authorization: Basic {encoded}"')

    print("\n" + "=" * 60)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    start_server(8000)
