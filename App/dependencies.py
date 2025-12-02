from fastapi import Depends
from sqlalchemy.orm import Session
from .database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Re-export auth dependencies for easy access
from .auth import get_current_user, oauth2_scheme