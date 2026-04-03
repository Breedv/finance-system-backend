# Finance System Backend

A REST API backend for managing and analyzing personal financial records, built with Flask, SQLAlchemy, and JWT authentication.

---

## Tech Stack

- **Python 3.12**
- **Flask** — web framework
- **Flask-SQLAlchemy** — ORM for database management
- **Flask-JWT-Extended** — JWT based authentication
- **SQLite** — lightweight local database
- **Werkzeug** — password hashing

---

## Project Structure

finance_system/
├── app/
│ ├── init.py # App factory, extensions
│ ├── models.py # Database models (User, Transaction)
│ ├── auth.py # Register and login routes
│ ├── transactions.py # CRUD and filter routes
│ ├── analytics.py # Summary and analytics routes
│ └── decorators.py # Role based access control
├── config.py # App configuration
├── run.py # Entry point
├── requirements.txt # Dependencies
└── README.md

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/finance-system-backend.git
cd finance-system-backend
```

### 2. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python run.py
```

The server will start at `http://127.0.0.1:5000`

---

## API Endpoints

### Auth

| Method | Endpoint         | Description             | Access |
| ------ | ---------------- | ----------------------- | ------ |
| POST   | `/auth/register` | Register a new user     | Public |
| POST   | `/auth/login`    | Login and get JWT token | Public |

### Transactions

| Method | Endpoint             | Description            | Access    |
| ------ | -------------------- | ---------------------- | --------- |
| POST   | `/transactions/`     | Create a transaction   | Admin     |
| GET    | `/transactions/`     | Get all transactions   | All roles |
| GET    | `/transactions/<id>` | Get single transaction | All roles |
| PUT    | `/transactions/<id>` | Update a transaction   | Admin     |
| DELETE | `/transactions/<id>` | Delete a transaction   | Admin     |

### Filters (query params on GET /transactions/)

| Param        | Example                  | Description                 |
| ------------ | ------------------------ | --------------------------- |
| `type`       | `?type=income`           | Filter by income or expense |
| `category`   | `?category=food`         | Filter by category          |
| `start_date` | `?start_date=2024-01-01` | Filter from date            |
| `end_date`   | `?end_date=2024-12-31`   | Filter to date              |

### Analytics

| Method | Endpoint                        | Description                     | Access         |
| ------ | ------------------------------- | ------------------------------- | -------------- |
| GET    | `/analytics/summary`            | Total income, expenses, balance | All roles      |
| GET    | `/analytics/category-breakdown` | Totals grouped by category      | Analyst, Admin |
| GET    | `/analytics/monthly`            | Totals grouped by month         | Analyst, Admin |
| GET    | `/analytics/recent`             | Last 5 transactions             | All roles      |

---

## User Roles

| Role      | Permissions                                        |
| --------- | -------------------------------------------------- |
| `viewer`  | View transactions and basic summary                |
| `analyst` | View transactions, filters, and detailed analytics |
| `admin`   | Full access — create, update, delete, manage       |

---

## Testing the API

Use [Postman](https://www.postman.com/) or any REST client.

### Step 1 — Register a user

```json
POST /auth/register
{
    "username": "adminuser",
    "password": "password123",
    "role": "admin"
}
```

### Step 2 — Login

```json
POST /auth/login
{
    "username": "adminuser",
    "password": "password123"
}
```

Copy the `access_token` from the response.

### Step 3 — Use the token

Add this header to all protected requests:
Authorization: Bearer <your_access_token>

---

## Assumptions Made

- Each transaction belongs to the user who created it (identified via JWT)
- Roles are assigned at registration time
- Dates follow the `YYYY-MM-DD` format
- Amount must always be a positive number
- Type must be either `income` or `expense`

---

## Author

Breed  
Built as part of a Python Backend Development assessment
