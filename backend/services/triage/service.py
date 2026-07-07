from typing import Dict, Any, Tuple

# Mapping of respiratory conditions to base triage levels
DISEASE_TO_TRIAGE = {
    "Normal": "GREEN",
    "Viral Cold": "GREEN",
    "Asthma": "YELLOW",
    "COPD": "YELLOW",
    "Pneumonia": "RED",
    "Tuberculosis": "RED",
    "TB": "RED"
}

def determine_triage_level(
    disease: str, 
    confidence: float, 
    patient_history: Dict[str, Any] = None
) -> Tuple[str, str]:
    """
    Deterministically maps a predicted disease to a triage level and actionable text.
    Returns a tuple of (Triage Level, Actionable Instruction).
    """
    if not patient_history:
        patient_history = {}

    disease_normalized = disease.title() if disease else "Unknown"
    
    # Handle alias
    if disease_normalized == "Tb":
        disease_normalized = "Tuberculosis"

    base_triage = DISEASE_TO_TRIAGE.get(disease_normalized, "YELLOW")
    
    # Escalate to RED if patient has severe symptoms regardless of base triage
    if patient_history.get("distress_level") == "high":
        base_triage = "RED"
        
    action_text = ""
    
    if base_triage == "RED":
        if disease_normalized in ["Tuberculosis", "TB"]:
            action_text = (
                "🔴 RED ALERT: High suspicion of Tuberculosis.\n"
                "- Instruct patient to WEAR A MASK immediately.\n"
                "- Isolate patient if possible.\n"
                "- Refer IMMEDIATELY for GeneXpert testing at the nearest DOTS center."
            )
        else:
            action_text = (
                "🔴 RED ALERT: High suspicion of severe respiratory infection (e.g., Pneumonia).\n"
                "- Refer immediately to the nearest Upazila Health Complex or hospital for X-ray and evaluation."
            )
    elif base_triage == "YELLOW":
        action_text = (
            f"🟡 YELLOW ALERT: Suspicion of {disease_normalized}.\n"
            "- Medical review is recommended.\n"
            "- Refer patient to a clinic or physician within 24–48 hours for a formal diagnosis."
        )
    elif base_triage == "GREEN":
        action_text = (
            "🟢 GREEN ALERT: Likely a common viral respiratory illness or normal breathing.\n"
            "- Recommend over-the-counter (OTC) symptom relief (e.g., Paracetamol, antihistamines).\n"
            "- DO NOT prescribe antibiotics.\n"
            "- Advise patient to return if symptoms worsen after 3 days."
        )
    else:
        base_triage = "YELLOW"
        action_text = (
            "🟡 YELLOW ALERT: Condition unclear.\n"
            "- Refer patient to a doctor for a proper clinical evaluation."
        )
        
    return base_triage, action_text

def validate_llm_triage(llm_triage: str, llm_disease: str) -> str:
    """
    Can be used to ensure the LLM doesn't downgrade a severe disease.
    E.g. If LLM says TB is GREEN, we override it to RED.
    """
    deterministic_triage, _ = determine_triage_level(llm_disease, confidence=1.0)
    
    # Hierarchy of severity
    severity = {"GREEN": 1, "YELLOW": 2, "RED": 3}
    
    llm_triage_upper = llm_triage.upper() if llm_triage else "YELLOW"
    
    if severity.get(deterministic_triage, 2) > severity.get(llm_triage_upper, 2):
        # Override if deterministic rule says it's worse
        return deterministic_triage
        
    return llm_triage_upper
