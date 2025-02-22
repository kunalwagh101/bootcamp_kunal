

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware


DATABASE_URL = "sqlite:///./test.db"  

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # I

Base.metadata.create_all(bind=engine)


class UserSchema(BaseModel):
    username: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title="Full-Stack FastAPI App")




"""
Adding Basic Authentication

Objective: Secure a Streamlit app with simple username and password authentication.
Task: Implement a login page that requires a username and password to access the main app content.
Expected Output: The main app content is only accessible after successful login.
"""

@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    """
    Registers a new user.
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = User(username="username", password="password")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserSchema, db: Session = Depends(get_db)):
    """
    Authenticates a user.
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user and db_user.password == user.password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
