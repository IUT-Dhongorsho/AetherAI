from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

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
