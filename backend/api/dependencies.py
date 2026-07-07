from backend.database.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

get_db_session = get_db

