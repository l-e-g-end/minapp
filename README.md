# 🛡️ MinApp — FastAPI Authentication & Role-Based Access Control

A lightweight, secure, and Docker-ready **FastAPI** application demonstrating:

- 🧾 **User Registration & Login** with JWT-based authentication
- 🔐 **Role-Based Access Control** (`user` vs `admin`)
- 🚀 **Asynchronous PostgreSQL** integration via `asyncpg` and `databases`
- 🧱 **SQLAlchemy ORM** models and **Pydantic** schemas
- 🪵 **Structured Logging** and **Rate Limiting** (5 requests/minute) using SlowAPI
- 🌐 **CORS** configured for enhanced security (only `GET` and `POST`)

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Project Structure](#-project-structure)
4. [Getting Started (Local)](#-getting-started-local)
5. [Docker Deployment](#-docker-deployment)
6. [Authentication Flow](#-authentication-flow)
7. [API Endpoints](#-api-endpoints)
8. [Security & Best Practices](#-security--best-practices)
9. [Limitations & Future Work](#-limitations--future-work)

---

## 🚀 Features

- **User Registration**: Securely register with `name`, `email`, and `password` (hashed via bcrypt).
- **JWT Login**: Obtain a JWT token with `/login` using OAuth2 password flow.
- **Protected Endpoints**: `/me` for authenticated users, `/admin-panel` for admin role only.
- **Asynchronous DB**: High-performance Postgres access with `asyncpg` and `databases`.
- **Rate Limiting**: 5 requests/minute per IP using **SlowAPI**.
- **Structured Logging**: Application events and requests logged to `app.log`.
- **CORS**: Only allows `GET` and `POST` methods from configured origins.

---

## 🧰 Tech Stack

| Component            | Technology                          |
|----------------------|-------------------------------------|
| Web Framework        | FastAPI                             |
| ASGI Server          | Uvicorn                             |
| Database             | PostgreSQL (asyncpg + databases)    |
| ORM                  | SQLAlchemy                          |
| Auth & Security      | Python-JOSE (JWT), Passlib (bcrypt) |
| Rate Limiting        | SlowAPI                             |
| Logging              | Python `logging`                    |
| Containerization     | Docker, Docker Compose              |

---

## 🗂️ Project Structure

```bash
minapp/
├── auth.py             # JWT and password hashing logic
├── database.py         # Async database setup
├── dependencies.py     # OAuth2 & role-based dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Local Docker Compose setup
├── main.py             # FastAPI application instance
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic request/response schemas
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── app.log             # Application logs
```

---

## 🏁 Getting Started (Local)

### Prerequisites

- Python 3.8+
- PostgreSQL database
- `virtualenv` (optional but recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/l-e-g-end/minapp.git
cd minapp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and set your PostgreSQL credentials and JWT settings:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/minapp_db
   SECRET_KEY=your-secure-random-secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

### Run Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Visit [`http://localhost:8080/docs`](http://localhost:8080/docs) for interactive API docs.

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
docker-compose up --build -d
```

- **App**: `http://localhost:8080`
- **PostgreSQL**: on host `db`, port `5432`

### Manual Docker

```bash
# Build image
docker build -t minapp .

# Run container
docker run -d \
  -p 8080:8080 \
  --env-file .env \
  minapp
```

---

## 🔑 Authentication Flow

1. **Register** (public): `POST /register`
   ```json
   { "name":"alice", "email":"alice@example.com", "password":"secret" }
   ```
2. **Login** (public): `POST /login` (form data)
   - Fields: `username` (email), `password`
   - Returns: `{ "access_token":"...","token_type":"bearer" }`
3. **Authorize** in Swagger UI: Click **Authorize**, enter:
   ```
   Bearer <access_token>
   ```
4. Access protected endpoints:
   - `GET /me`
   - `GET /admin-panel` (requires admin role)

---

## 📚 API Endpoints

| Method | Endpoint       | Auth       | Description                 |
| ------ | -------------- | ---------- | --------------------------- |
| POST   | `/register`    | ❌ Public   | Create a new user           |
| POST   | `/login`       | ❌ Public   | Obtain JWT token            |
| GET    | `/me`          | ✅ JWT      | Get current user profile    |
| GET    | `/admin-panel` | ✅ JWT + Admin | Admin-only access         |

---

## 🔒 Security & Best Practices

- **Password Hashing**: bcrypt with Passlib
- **JWT**: signed tokens, short expiry
- **CORS**: only `GET`, `POST` allowed from trusted origins
- **Rate Limiting**: 5 requests/minute/IP via SlowAPI
- **Logging**: all critical events to `app.log`
- **Env Config**: secrets in `.env`, not in source

---

## 🔮 Limitations & Future Work

- Add refresh tokens & token revocation
- Email verification & password reset flows
- More granular permissions & roles
- Migrations with Alembic
- Production-grade logging & monitoring (e.g., ELK stack)
- Automated tests (unit & integration)


