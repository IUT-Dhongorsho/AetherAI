"""
Fallback Triage Logic for AetherAI.
Maps acoustic predictions (crackles/wheezes) + symptoms to Red/Yellow/Green.
This runs as a safety net if the Diagnosis Agent fails.
"""

from typing import Dict, Any, Tuple

def determine_triage(
    audio_prediction: Dict[str, float], 
    patient_history: Dict[str, Any]
) -> Tuple[str, str, str]:
    """
    Returns: (triage_level, action_text, color_code)
    """
    # Extract confidence scores
    crackles = audio_prediction.get("crackles", 0.0)
    wheezes = audio_prediction.get("wheezes", 0.0)
    normal = audio_prediction.get("normal", 0.0)
    
    # Extract symptoms
    fever = patient_history.get("fever", False)
    duration = patient_history.get("duration_days", 0)
    weight_loss = patient_history.get("weight_loss", False)
    
    # === RED ALERT: Suspected TB or Severe Pneumonia ===
    # High crackles + Fever + Duration > 14 days
    if crackles > 0.7 and fever and duration >= 14:
        return (
            "RED",
            "REFER FOR GENEXPERT TEST AT UPAZILA HEALTH COMPLEX. ISOLATE PATIENT.",
            "🔴"
        )
    
    # Severe crackles (> 0.85) with fever
    if crackles > 0.85 and fever:
        return (
            "RED",
            "URGENT: SUSPECTED PNEUMONIA. REFER FOR CHEST X-RAY AND BLOOD TEST IMMEDIATELY.",
            "🔴"
        )
    
    # === YELLOW ALERT: Needs clinic within 48 hours ===
    if crackles > 0.6 or (wheezes > 0.7 and fever):
        return (
            "YELLOW",
            "MODERATE RISK. VISIT NEAREST UPAZILA HEALTH COMPLEX WITHIN 48 HOURS.",
            "🟡"
        )
    
    # === GREEN ALERT: Viral / OTC ===
    if normal > 0.7 or (wheezes > 0.5 and not fever):
        return (
            "GREEN",
            "LIKELY VIRAL COLD OR MILD ASTHMA. DO NOT PRESCRIBE ANTIBIOTICS. REST & PARACETAMOL.",
            "🟢"
        )
    
    # Catch-all fallback
    return (
        "YELLOW",
        "INCONCLUSIVE RESULT. PLEASE RE-ASSESS OR REFER TO CLINIC.",
        "🟡"
    )
