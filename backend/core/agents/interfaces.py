"""
THE GOLDEN CONTRACT - With MOCK implementations.
This allows the server to boot RIGHT NOW without waiting for agents.
When your friend finishes his agents, he just replaces these mock functions.
"""

from typing import Dict, Any, Callable, TypedDict, List, Optional

class PatientState(TypedDict, total=False):
    patient_id: str
    audio_path: str
    pharmacist_notes: str
    patient_history: Dict[str, Any]
    audio_features: Dict[str, Any]
    audio_prediction: Dict[str, float]
    transcript: str
    nlp_features: Dict[str, Any]
    retrieved_docs: List[Dict[str, str]]
    diagnosis: Dict[str, Any]
    triage_level: str
    action_text: str
    citations: List[str]
    current_agent: str
    is_complete: bool

AgentFunction = Callable[[PatientState], PatientState]

# ---------- MOCK IMPLEMENTATIONS ----------
# These run until your friend overwrites them with real logic.
# He must replace these with his actual agent.py functions.

def intake_agent(state: PatientState) -> PatientState:
    state["patient_history"] = {
        "age": 45,
        "fever": True,
        "duration_days": 14,
        "weight_loss": True
    }
    return state

def audio_analyst(state: PatientState) -> PatientState:
    state["audio_prediction"] = {"crackles": 0.85, "wheezes": 0.10, "normal": 0.05}
    state["audio_features"] = {"sample_rate": 16000, "duration": 5.0}
    return state

def symptom_classifier(state: PatientState) -> PatientState:
    state["transcript"] = "amar dui semana dhore khasi, jar shathe jor"
    state["nlp_features"] = {"entities": ["cough", "fever"], "distress": "moderate"}
    return state

def rag_retriever(state: PatientState) -> PatientState:
    state["retrieved_docs"] = [{
        "title": "BD NTP Guideline",
        "snippet": "Cough >14 days with fever is presumptive TB."
    }]
    return state

def diagnosis_agent(state: PatientState) -> PatientState:
    state["diagnosis"] = {"primary": "Tuberculosis", "confidence": 0.82}
    state["triage_level"] = "RED"
    state["action_text"] = "REFER FOR GENEXPERT TEST AT UPAZILA HEALTH COMPLEX"
    state["citations"] = ["BD NTP Guideline 2024, Section 3.2"]
    return state
