from sqlalchemy.orm import Session
from backend.database.models import Patient, ChatHistory, TestResult
from datetime import datetime
from typing import Optional, List, Dict, Any

def create_patient(db: Session, patient_id: str, age: Optional[int] = None, gender: Optional[str] = None, fever_status: Optional[bool] = None, smoker_status: Optional[bool] = None, language_preference: Optional[str] = "English") -> Patient:
    patient = Patient(
        id=patient_id,
        age=age,
        gender=gender,
        fever_status=fever_status,
        smoker_status=smoker_status,
        language_preference=language_preference,
        created_at=datetime.utcnow()
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient(db: Session, patient_id: str) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == patient_id).first()

def add_chat_message(db: Session, patient_id: str, role: str, content: str) -> ChatHistory:
    message = ChatHistory(
        patient_id=patient_id,
        role=role,
        content=content,
        timestamp=datetime.utcnow()
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_chat_history(db: Session, patient_id: str, limit: int = 10) -> List[ChatHistory]:
    # Get last `limit` messages, ordered by timestamp ascending
    return db.query(ChatHistory).filter(ChatHistory.patient_id == patient_id).order_by(ChatHistory.timestamp.asc()).limit(limit).all()

def add_test_result(db: Session, patient_id: str, test_type: str, results: Dict[str, Any]) -> TestResult:
    result = TestResult(
        patient_id=patient_id,
        test_type=test_type,
        results=results,
        timestamp=datetime.utcnow()
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
