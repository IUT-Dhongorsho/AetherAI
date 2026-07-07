"""
AetherAI Patient State - The "Shared Memory" for all 5 Agents.
This is passed between every node in the LangGraph workflow.
"""

from typing import TypedDict, Optional, Dict, Any, List

class PatientState(TypedDict, total=False):
    # === Inputs (Set by the user/pharmacist) ===
    patient_id: str
    audio_path: str                     # Path to the uploaded .wav cough audio
    pharmacist_notes: str               # Extra text typed by pharmacist
    
    # === Agent 1: Intake Agent (Collects history) ===
    patient_history: Dict[str, Any]     # e.g., {"age": 45, "fever": True, "duration_days": 14}
    
    # === Agent 2: Audio Analyst (CNN on sound) ===
    audio_features: Dict[str, Any]      # e.g., {"mfcc_mean": [...], "spectrogram_url": "..."}
    audio_prediction: Dict[str, float]  # e.g., {"crackles": 0.85, "wheezes": 0.10, "normal": 0.05}
    
    # === Agent 3: Symptom Classifier (NLP on transcript) ===
    transcript: str                     # Bangla text from Whisper
    nlp_features: Dict[str, Any]        # e.g., {"entities": ["fever", "cough"], "distress_level": "high"}
    
    # === Agent 4: RAG Retriever (Guidelines) ===
    retrieved_docs: List[Dict[str, str]] # e.g., [{"title": "BD NTP Guideline", "snippet": "Cough >14 days..."}]
    
    # === Agent 5: Diagnosis Agent (Final Decision) ===
    diagnosis: Dict[str, Any]           # e.g., {"primary": "TB", "confidence": 0.87, "differentials": ["Pneumonia"]}
    triage_level: str                   # "RED", "YELLOW", "GREEN"
    action_text: str                    # "REFER FOR GENEXPERT"
    citations: List[str]                # ["WHO Pneumonia Guideline 2023"]
    
    # === Routing State (for potential future loops) ===
    current_agent: str
    is_complete: bool
