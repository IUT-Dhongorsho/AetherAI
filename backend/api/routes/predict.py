import os
import uuid
import shutil
from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from backend.api.dependencies import get_db_session
from backend.core.graph.workflow import app_graph
from backend.core.graph.state import PatientState
from backend.database.models import Patient, Diagnosis
from backend.config import settings
from backend.services.reporting.service import generate_pdf_report
from backend.services.triage.service import determine_triage  # <-- NEW FALLBACK

router = APIRouter()

@router.post("/predict")
async def predict(
    audio: UploadFile = File(...),
    pharmacist_notes: str = Form(""),
    age: int = Form(None),
    gender: str = Form(None),
    region: str = Form(None),
    phone: str = Form(None),  # For notification later
    db: Session = Depends(get_db_session)
):
    # 1. Validate audio
    if not audio.filename.endswith(('.wav', '.mp3', '.m4a')):
        raise HTTPException(400, "Only audio files (wav, mp3, m4a) are allowed.")
    
    # 2. Save audio
    os.makedirs(settings.AUDIO_UPLOAD_DIR, exist_ok=True)
    patient_id = str(uuid.uuid4())[:8]
    file_ext = audio.filename.split('.')[-1]
    file_name = f"{patient_id}.{file_ext}"
    file_path = os.path.join(settings.AUDIO_UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    
    # 3. Initial State
    initial_state: PatientState = {
        "patient_id": patient_id,
        "audio_path": file_path,
        "pharmacist_notes": pharmacist_notes,
        "patient_history": {
            "age": age,
            "gender": gender,
            "region": region
        }
    }
    
    # 4. Run Agents
    try:
        result_state = app_graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(500, f"Agent pipeline failed: {str(e)}")
    
    # 5. --- SAFETY NET: Fallback Triage ---
    # If the Diagnosis Agent didn't return triage or returned garbage,
    # we overwrite it using our deterministic fallback service.
    audio_pred = result_state.get("audio_prediction", {})
    history = result_state.get("patient_history", {})
    
    if not result_state.get("triage_level") or result_state.get("triage_level") == "UNKNOWN":
        fallback_level, fallback_action, _ = determine_triage(audio_pred, history)
        result_state["triage_level"] = fallback_level
        result_state["action_text"] = fallback_action
        result_state["diagnosis"] = {
            "primary": "Fallback Triage", 
            "confidence": max(audio_pred.values()) if audio_pred else 0.5
        }
        result_state["citations"] = ["AetherAI Fallback Triage Engine"]

    # 6. Save to DB
    patient = Patient(
        id=patient_id,
        age=age,
        gender=gender,
        region=region,
        created_at=datetime.utcnow()
    )
    db.add(patient)
    
    diagnosis = Diagnosis(
        patient_id=patient_id,
        timestamp=datetime.utcnow(),
        prediction=result_state.get("audio_prediction", {}),
        triage_level=result_state.get("triage_level", "UNKNOWN"),
        action_text=result_state.get("action_text", ""),
        diagnosis_text=result_state.get("diagnosis", {}).get("primary", ""),
        confidence=result_state.get("diagnosis", {}).get("confidence", 0.0),
        citations=result_state.get("citations", [])
    )
    db.add(diagnosis)
    db.commit()
    db.refresh(diagnosis)
    
    # 7. Generate PDF
    pdf_path = generate_pdf_report(
        patient_id=patient_id,
        diagnosis_text=diagnosis.diagnosis_text,
        confidence=diagnosis.confidence,
        triage_level=diagnosis.triage_level,
        action_text=diagnosis.action_text,
        citations=diagnosis.citations
    )
    
    # 8. Return
    return {
        "patient_id": patient_id,
        "triage_level": result_state.get("triage_level"),
        "diagnosis": result_state.get("diagnosis"),
        "action_text": result_state.get("action_text"),
        "citations": result_state.get("citations", []),
        "pdf_report_url": f"/reports/{os.path.basename(pdf_path)}"
    }
