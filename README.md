# MoMo SMS Data Project

## Team name
TriTech Minds

## Authors
- Kami Pacifique
- Gasangwa Teta Duice
- Ndahiro Prince

## Project Description 
This application processes MoMo SMS messages provided in the XML format. The sytsem extracts, cleans, categorizes and stores data transactions in a relational database. This application will help users understand their mobile money activity. 


## System Architecture
The high level system architecture illustrates how data flows from MoMo SMS XML files through a backend ETL pipeline into a database and finally to a frontend dashboard for visualization.

## Architecture Diagram Link:
https://drive.google.com/file/d/11gXr3FizgGrb0v-2IhxBHvHUFHglbfu-/view

## Scrum Board(Agile planning)
Our team uses Agile scrum board to track tasks and collaboration throughout the project lifecycle.

## Scrum Board Link:
https://github.com/users/KamiPacifique/projects/2/views/1

## Database Design
The MoMo SMS database manages mobile money transcations with a relational design. It includes users, transactions categories, transctions, tags, transction-tags, and system logs. Users and transactions are linked via foreign keys, categories classify transaction types, and tags allow flexible labeling. Constrints enforce valid formats, positive amounts, and controlled statuses, while indexes improve query performance. System logs ensure auditability, making the design robust, consistent, and traceable.

## Team Logbook link
- Database Design and Implementation: https://docs.google.com/spreadsheets/d/1T1PYaiUr_BibOAKgpvWyrgsloJ9IxkUUGLgMesFs5u0/edit?usp=sharing
- Building and Securing a REST API:
https://docs.google.com/spreadsheets/d/1azmRzRzOGVMqhv7s2NPgLFo4FMgL9ayGmC4vb23SEgU/edit?usp=sharing 

## Documentation link
https://github.com/KamiPacifique/Momo-Sms-Data/blob/main/Docs/Documentation.pdf

## Setup Instructions 

1. Clone the project 
    - In your terminal input: git clone https://github.com/KamiPacifique/Momo-Sms-Data.git
    -Press Enter
2. Open the project folder 
    - Type cd Momo-Sms-Data
    - Press Enter 
3. Install required packages (if needed)
    - Type: pip install -r requirements.txt
    - Press Enter 
4. Start the server
    - Type: python3 momo_api.py
    - Press Enter
    - You should see a message saying the server is running
5. The API is ready!
    - Open your browser and go to: http://localhost:8000
    - Or use Postman or any API testing tool

### Login Information 
| Username | Password |
|----------|----------|
|Admin     |admin123  |
|user      |user456   |
|test      |test789   |

Use these to access the API. 

### API Endpoints
The API provides full CRUD operations for transaction management:

- GET /transactions - List all transactions
- GET /transactions/{id} - Get specific transaction details
- POST /transactions - Create new transaction (requires: amount, transaction_type, sender, receiver)
- PUT /transactions/{id} - Update existing transaction
- DELETE /transactions/{id} - Delete transaction

Required fields for creating transactions: amount, transaction_type, sender, receiver
Optional fields: currency (default: RWF), status (default: pending), timestamp, reference

Testing tools: Use cURL, Postman, Python requests, or any HTTP client with Basic Authentication.

### Configuration 
Change port: Edit momo_api.py and modify start_server(8080) to desired port
Add users: Edit API_USERS dictionary in momo_api.py

## Project Status
## Phase 1: Planning & Setup (done)
- Repository created and collaborators added
- Architecture diagram designed
- Scrum board initialized 

## Phase 2: Database design, ERD diagram, and JSON file (done)
- Draw an ERD diagram 
- Create a database design and SQL tables
- Edit the JSON file

## Phase 3: Building and Securing a REST API (current)
-Setup Instructions

in coming phases we will focus on backend development, data processing, and frontend components. The directory structure will evolve as development progresses.
