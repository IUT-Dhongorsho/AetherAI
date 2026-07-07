from backend.database.models import get_db
from backend.config import settings
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()
