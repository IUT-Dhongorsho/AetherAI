from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api.dependencies import get_db_session
from backend.database.models import Patient, Diagnosis

router = APIRouter()

@router.get("/history/{patient_id}")
def get_patient_history(patient_id: str, db: Session = Depends(get_db_session)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(404, "Patient not found")
    
    diagnoses = db.query(Diagnosis).filter(Diagnosis.patient_id == patient_id).all()
    
    return {
        "patient": {
            "id": patient.id,
            "age": patient.age,
            "gender": patient.gender,
            "region": patient.region,
            "created_at": patient.created_at
        },
        "diagnoses": [
            {
                "timestamp": d.timestamp,
                "diagnosis": d.diagnosis_text,
                "confidence": d.confidence,
                "triage_level": d.triage_level,
                "action_text": d.action_text,
                "citations": d.citations
            } for d in diagnoses
        ]
    }
