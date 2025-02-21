"""

NO.5 Database Integration

Objective: Integrate a simple database (e.g., SQLite) with FastAPI for persisting data.
Task: Connect FastAPI to a SQLite database and modify CRUD operations to use the database.
Expected Output: CRUD operations interact with a SQLite database. (To add, update, and delete items),
from sqlalchemy import create_engine
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
