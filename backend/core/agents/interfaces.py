"""
The Golden Contract for All Agents.

Every agent must accept the PatientState dictionary and return the updated dictionary.
This allows the LangGraph orchestrator to chain them seamlessly.
"""

from typing import Dict, Any, Callable, TypedDict, Optional, List

# --- Define the Shared State Structure (Mirrors backend/core/graph/state.py) ---
class PatientState(TypedDict, total=False):
    # Inputs
    patient_id: str
    audio_path: str                     # Path to uploaded .wav file
    transcript: str                     # Whisper transcribed Bangla text
    
    # Intake Agent outputs
    patient_history: Dict[str, Any]     # e.g., {"age": 45, "fever": True, "duration_days": 14}
    
    # Audio Analyst outputs
    audio_features: Dict[str, Any]      # e.g., {"mfcc": [...], "spectrogram": "..."}
    audio_prediction: Dict[str, float]  # e.g., {"crackles": 0.85, "wheezes": 0.10, "normal": 0.05}
    
    # Symptom Classifier outputs
    nlp_features: Dict[str, Any]        # e.g., {"entities": ["fever", "cough"], "sentiment": "distressed"}
    
    # RAG Retriever outputs
    retrieved_docs: List[Dict[str, str]] # e.g., [{"title": "BD NTP Guideline", "content": "..."}]
    
    # Diagnosis Agent outputs
    diagnosis: Dict[str, Any]           # e.g., {"primary": "TB", "confidence": 0.87}
    triage_level: str                   # "RED", "YELLOW", "GREEN"
    action_text: str                    # Actionable instruction for pharmacist
    citations: List[str]                # e.g., ["WHO Guideline 2023, p. 12"]

# --- The Function Signature (The Contract) ---
# Every agent function MUST accept a PatientState dict and return a PatientState dict.
AgentFunction = Callable[[PatientState], PatientState]

# --- Type hints for your teammate to follow ---
def intake_agent(state: PatientState) -> PatientState: ...
def audio_analyst(state: PatientState) -> PatientState: ...
def symptom_classifier(state: PatientState) -> PatientState: ...
def rag_retriever(state: PatientState) -> PatientState: ...
def diagnosis_agent(state: PatientState) -> PatientState: ...
