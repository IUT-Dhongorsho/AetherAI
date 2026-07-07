from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from backend.config import settings

# Setup Database Engine
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Returns a new database session."""
    return SessionLocal()

# --- Models ---

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True, index=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    region = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Diagnosis(Base):
    __tablename__ = "diagnoses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    prediction = Column(JSON, nullable=True)
    triage_level = Column(String, nullable=True)
    action_text = Column(Text, nullable=True)
    diagnosis_text = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    citations = Column(JSON, nullable=True)
