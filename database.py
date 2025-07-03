from databases import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

DATABASE_URL = "postgresql+asyncpg://postgres:admin@localhost:5432/mydatabase"

database = Database(DATABASE_URL)

Base = declarative_base()

# Sync engine (used only for creating tables via metadata)
SYNC_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")
engine = create_engine(SYNC_DATABASE_URL)
