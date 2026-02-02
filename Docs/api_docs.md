## Setup Instructions

### 1. Save the API Script

Save the provided Python code as `momo_api.py`

### 2. Make it Executable (Optional)

```bash
chmod +x momo_api.py
```

### 3. Run the Server

```bash
python3 momo_api.py
```

The server will start on `http://localhost:8000`

### 4. Verify Server is Running

You should see output like:

```
============================================================
MOBILE MONEY TRANSACTION API
============================================================
Server: http://localhost:8000
Transactions: 3

ENDPOINTS:
  GET    /transactions         - List all transactions
  GET    /transactions/{id}    - Get specific transaction
  POST   /transactions         - Create new transaction
  PUT    /transactions/{id}    - Update transaction
  DELETE /transactions/{id}    - Delete transaction
============================================================
```

## Authentication

The API uses Basic Authentication. Three test users are available:

| Username | Password  |
|----------|-----------|
| admin    | admin123  |
| user     | user456   |
| test     | test789   |

## API Endpoints

### 1. List All Transactions

**GET** `/transactions`

```bash
curl -X GET "http://localhost:8000/transactions" \
  -H "Authorization: Basic YWRtaW46YWRtaW4xMjM="
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "count": 3,
    "transactions": [
      {
        "id": "1001",
        "amount": 2000.0,
        "transaction_type": "received",
        "sender": "Jane Smith",
        "receiver": "John Doe",
        "timestamp": "2024-05-10T16:30:58",
        "currency": "RWF",
        "status": "completed",
        "reference": "TXN001"
      }
    ]
  }
}
```

### 2. Get Single Transaction

**GET** `/transactions/{id}`

```bash
curl -X GET "http://localhost:8000/transactions/1001" \
  -H "Authorization: Basic YWRtaW46YWRtaW4xMjM="
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": "1001",
    "amount": 2000.0,
    "transaction_type": "received",
    "sender": "Jane Smith",
    "receiver": "John Doe",
    "timestamp": "2024-05-10T16:30:58",
    "currency": "RWF",
    "status": "completed",
    "reference": "TXN001"
  }
}
```

### 3. Create New Transaction

**POST** `/transactions`

```bash
curl -X POST "http://localhost:8000/transactions" \
  -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 3500.0,
    "transaction_type": "sent",
    "sender": "John Doe",
    "receiver": "Bob Wilson",
    "currency": "RWF"
  }'
```

**Required Fields:**
- `amount` (number)
- `transaction_type` (string)
- `sender` (string)
- `receiver` (string)

**Optional Fields:**
- `currency` (default: "RWF")
- `status` (default: "pending")
- `timestamp` (default: current time)
- `reference` (default: auto-generated)

**Response:**
```json
{
  "status": "success",
  "message": "Transaction created",
  "data": {
    "id": "1004",
    "amount": 3500.0,
    "transaction_type": "sent",
    "sender": "John Doe",
    "receiver": "Bob Wilson",
    "timestamp": "2024-05-11T10:30:00",
    "currency": "RWF",
    "status": "pending",
    "reference": "TXN1004"
  }
}
```

### 4. Update Transaction

**PUT** `/transactions/{id}`

```bash
curl -X PUT "http://localhost:8000/transactions/1001" \
  -H "Authorization: Basic YWRtaW46YWRtaW4xMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "amount": 2500.0
  }'
```

**Updatable Fields:**
- `amount`
- `transaction_type`
- `sender`
- `receiver`
- `currency`
- `status`
- `timestamp`

**Response:**
```json
{
  "status": "success",
  "message": "Transaction updated",
  "data": {
    "id": "1001",
    "amount": 2500.0,
    "transaction_type": "received",
    "sender": "Jane Smith",
    "receiver": "John Doe",
    "timestamp": "2024-05-10T16:30:58",
    "currency": "RWF",
    "status": "completed",
    "reference": "TXN001"
  }
}
```

### 5. Delete Transaction

**DELETE** `/transactions/{id}`

```bash
curl -X DELETE "http://localhost:8000/transactions/1001" \
  -H "Authorization: Basic YWRtaW46YWRtaW4xMjM="
```

**Response:**
```json
{
  "status": "success",
  "message": "Transaction deleted"
}
```

## Pre-loaded Test Data

The API starts with 3 transactions:

1. **Transaction 1001**: Received 2000 RWF from Jane Smith
2. **Transaction 1002**: Sent 1000 RWF to Alice Brown
3. **Transaction 1003**: Deposited 5000 RWF from Bank

## Error Responses

### 401 Unauthorized
```json
{
  "status": "error",
  "message": "Authentication failed"
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Transaction not found"
}
```

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Invalid JSON data"
}
```

## Testing with Different Tools

### Using Python requests

```python
import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:8000/transactions"
auth = HTTPBasicAuth('admin', 'admin123')

# Get all transactions
response = requests.get(url, auth=auth)
print(response.json())

# Create new transaction
new_transaction = {
    "amount": 1500.0,
    "transaction_type": "sent",
    "sender": "Alice",
    "receiver": "Bob",
    "currency": "RWF"
}
response = requests.post(url, json=new_transaction, auth=auth)
print(response.json())
```

### Using Postman

1. Set request type (GET, POST, PUT, DELETE)
2. Enter URL: `http://localhost:8000/transactions`
3. Go to **Authorization** tab
4. Select **Basic Auth**
5. Enter username and password
6. For POST/PUT, add JSON body in **Body** tab (select **raw** and **JSON**)

### Using JavaScript/Fetch

```javascript
const username = 'admin';
const password = 'admin123';
const auth = btoa(`${username}:${password}`);

fetch('http://localhost:8000/transactions', {
  headers: {
    'Authorization': `Basic ${auth}`
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Configuration

### Change Port

Edit the last line in `momo_api.py`:

```python
if __name__ == "__main__":
    start_server(8080)  # Change to desired port
```

### Add/Modify Users

Edit the `API_USERS` dictionary in the `MomoAPIHandler` class:

```python
API_USERS = {
    "admin": "admin123",
    "user": "user456",
    "test": "test789",
    "newuser": "newpass"  # Add new user
}
```

### Modify Initial Transactions

Edit the `transactions_store` dictionary in the `MomoAPIHandler` class.

## Troubleshooting

### Server won't start

- Check if port 8000 is already in use
- Try a different port: `start_server(8001)`
- Ensure Python 3.6+ is installed: `python3 --version`

### Authentication fails

- Ensure you're using the correct username:password combination
- Check that the Authorization header is properly formatted
- Use the exact base64 strings shown when the server starts

### Connection refused

- Verify the server is running
- Check the correct URL: `http://localhost:8000`
- Ensure firewall isn't blocking the port

