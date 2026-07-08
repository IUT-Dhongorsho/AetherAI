from sqlalchemy import Column, String, Integer, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

# --- Models ---

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True, index=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    fever_status = Column(Boolean, nullable=True)
    smoker_status = Column(Boolean, nullable=True)
    language_preference = Column(String, nullable=True) # "Bangla" or "English"
    created_at = Column(DateTime, default=datetime.utcnow)
    
    chat_history = relationship("ChatHistory", back_populates="patient", cascade="all, delete-orphan")
    test_results = relationship("TestResult", back_populates="patient", cascade="all, delete-orphan")

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    message_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    role = Column(String, nullable=False) # 'user', 'model', 'system'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="chat_history")

class TestResult(Base):
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    test_type = Column(String, nullable=False) # e.g. "vitals", "cough"
    results = Column(JSON, nullable=False)
    
    patient = relationship("Patient", back_populates="test_results")
