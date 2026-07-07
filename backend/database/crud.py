from sqlalchemy.orm import Session
from backend.database.models import Patient, Diagnosis
from datetime import datetime
from typing import Optional, List, Dict, Any

def create_patient(db: Session, patient_id: str, age: Optional[int], gender: Optional[str], region: Optional[str]) -> Patient:
    patient = Patient(
        id=patient_id,
        age=age,
        gender=gender,
        region=region,
        created_at=datetime.utcnow()
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient(db: Session, patient_id: str) -> Optional[Patient]:
    return db.query(Patient).filter(Patient.id == patient_id).first()

def create_diagnosis(
    db: Session,
    patient_id: str,
    prediction: Dict[str, Any],
    triage_level: str,
    action_text: str,
    diagnosis_text: str,
    confidence: float,
    citations: List[Any]
) -> Diagnosis:
    diagnosis = Diagnosis(
        patient_id=patient_id,
        timestamp=datetime.utcnow(),
        prediction=prediction,
        triage_level=triage_level,
        action_text=action_text,
        diagnosis_text=diagnosis_text,
        confidence=confidence,
        citations=citations
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    return diagnosis

def get_diagnoses_for_patient(db: Session, patient_id: str) -> List[Diagnosis]:
    return db.query(Diagnosis).filter(Diagnosis.patient_id == patient_id).all()
