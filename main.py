from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import database
import models
import schemas
import auth
from dependencies import get_current_active_user, get_admin_user
from database import Base, engine

import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),   # log to file
        logging.StreamHandler()           # log to console
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Implement CORS for security reasons
app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_methods = ["GET", "POST"],
        allow_headers = ["*"]
        )

# Create tables (only necessary in dev if not using Alembic)
Base.metadata.create_all(bind=engine)

# Startup event to connect to the DB
@app.on_event("startup")
async def startup():
    await database.database.connect()
    logger.info("[*] Database connected.")

# Shutdown event to disconnect from the DB
@app.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()
    logger.info("[*] Database disconnected.")

# Register a new user
@app.post("/register", response_model=schemas.UserOut)
@limiter.limit("5/minute")
async def register(request: Request, user: schemas.UserCreate):
    hashed = auth.hash_password(user.password)

    query = models.User.__table__.insert().values(
        name=user.name,
        email=user.email,
        hashed_password=hashed,
        role="user"
    )

    user_id = await database.database.execute(query)

    logger.info(f"[+] New user registered: {user.email} (id: {user_id})")

    return {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "role": "user"
    }

# Login and get JWT token
@app.post("/login", response_model=schemas.Token)
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm uses 'username' field → we use email for login
    query = select(models.User).where(
            (models.User.email == form_data.username) | 
            (models.User.name == form_data.username)
            )
    user = await database.database.fetch_one(query)



    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        logger.info(f"[x] Failed login attempt: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info(f"[+] Successfuly loggin: {user.email}")
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Get current logged-in user's profile
@app.get("/me", response_model=schemas.UserOut)
@limiter.limit("5/minute")
async def read_users_me(request: Request, current_user=Depends(get_current_active_user)):
    return dict(current_user)


# Admin-only endpoint
@app.get("/admin-panel")
@limiter.limit("5/minute")
async def admin_panel(request: Request, admin=Depends(get_admin_user)):
    logger.info(f"[***] Admin access granted to: {admin['email']}")
    return {"message": f"Welcome Admin {admin['name']}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=False) # Set reload to True => without interruption

