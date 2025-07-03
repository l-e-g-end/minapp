# 🔐 FastAPI Auth & Role-Based Access Control

A minimal but powerful authentication system built with **FastAPI**, supporting:

- JWT-based authentication
- Role-based access (admin/user)
- Password hashing (bcrypt)
- Secure PostgreSQL connection (async)
- Rate limiting with `slowapi`
- Logging and monitoring
- CORS restriction (GET/POST only)

Perfect for those learning secure web development.

---------------------------------------------------------

## 📦 Features

- 🧑 User registration with hashed passwords
- 🔐 Login with JWT token issuance
- 🛡️ Protected routes for authenticated users (`/me`)
- 👮 Admin-only endpoint (`/admin-panel`)
- 🌐 CORS restriction (POST & GET only)
- ⚙️ Logging to `app.log`
- 🚨 Rate limiting (5 requests/minute per endpoint)
- 🗃️ PostgreSQL (via SQLAlchemy + Databases)
- 🐳 Dockerized for easy deployment

---------------------------------------------------------

### 📂 Project Structure

```bash
Mini-Project
├── main.py # Main FastAPI app
├── auth.py # Auth logic (JWT, hashing)
├── models.py # SQLAlchemy models
├── schemas.py # Pydantic schemas
├── database.py # Database setup
├── dependencies.py # Current user & admin logic
├── log # Logs (app.log file is located)
├── requirements.txt # Requirements for FastAPI app
├── Dockerfile # Docker image
├── docker-compose.yml # Full-stack with PostgreSQL
└── README.md # You're reading it!
```

---------------------------------------------------------

## 🚀 Getting Started

---------------------------------------------------------

### 🔧 Requirements


- Python 3.11+
- PostgreSQL (locally or via Docker)

### ⬇️ Install & Run Locally

# Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
# Install dependencies
```bash
pip install -r requirements.txt
```

# Run app
```
python main.py
```

---------------------------------------------------------

# 🔑 Register a User
Use /register route via Swagger UI or cURL:
```bash
curl -X POST http://localhost:8080/register \
-H "Content-Type: application/json" \
-d '{"name": "john", "email": "john@doe.com", "password": "strongpassword"}'
```

---------------------------------------------------------

### Optional, run via Docker

#### Build and start
```bash
docker-compose up --build
```

