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
    Implements deterministic rules for patient triage.
    
    Inputs:
        audio_prediction: Dictionary containing class probabilities (e.g. Normal, Pneumonia, Tuberculosis, Asthma, COPD, or crackles, wheezes, normal)
        patient_history: Dictionary containing patient history details (e.g. fever, duration_days, weight_loss)
        
    Returns:
        (triage_level, action_text, emoji)
    """
    # Extract confidence scores
    # Support both acoustic biomarkers (crackles, wheezes, normal) and predicted diseases
    crackles = audio_prediction.get(
        "crackles", 
        max(audio_prediction.get("Tuberculosis", 0.0), audio_prediction.get("Pneumonia", 0.0))
    )
    wheezes = audio_prediction.get(
        "wheezes", 
        max(audio_prediction.get("Asthma", 0.0), audio_prediction.get("COPD", 0.0))
    )
    normal = audio_prediction.get(
        "normal", 
        audio_prediction.get("Normal", 0.0)
    )
    
    # Extract symptoms
    fever = patient_history.get("fever", False)
    duration = patient_history.get("duration_days", patient_history.get("duration", 0))
    if isinstance(duration, str) and duration.isdigit():
        duration = int(duration)
    elif not isinstance(duration, (int, float)):
        duration = 0
        
    # === RED ALERT ===
    # Rule 1: High crackles + Fever + Duration >= 14 days -> Refer for GeneXpert
    if crackles > 0.7 and fever and duration >= 14:
        return (
            "RED",
            "REFER IMMEDIATELY FOR GENEXPERT TESTING AT NEAREST UPAZILA HEALTH COMPLEX. WEAR A MASK AND ISOLATE.",
            "🔴"
        )
    
    # Rule 2: Severe crackles (> 0.85) with fever -> Refer for Chest X-ray
    if crackles > 0.85 and fever:
        return (
            "RED",
            "URGENT: SUSPECTED SEVERE PNEUMONIA. REFER FOR CHEST X-RAY AND CLINICAL EVALUATION IMMEDIATELY.",
            "🔴"
        )
    
    # === YELLOW ALERT ===
    # Rule 3: Moderate risk (crackles > 0.6 or wheezes > 0.7 with fever) -> Visit clinic within 48 hours
    if crackles > 0.6 or (wheezes > 0.7 and fever):
        return (
            "YELLOW",
            "MODERATE RISK RESPIRATORY INDICATION. VISIT NEAREST CLINIC OR UPAZILA HEALTH COMPLEX WITHIN 48 HOURS.",
            "🟡"
        )
    
    # === GREEN ALERT ===
    # Rule 4: Low risk (normal > 0.7 or wheezes > 0.5 without fever) -> Viral / OTC medication, no antibiotics
    if normal > 0.7 or (wheezes > 0.5 and not fever):
        return (
            "GREEN",
            "LIKELY VIRAL COLD OR MILD ASTHMA. DO NOT PRESCRIBE ANTIBIOTICS. RECOMMENDED OTC TREATMENT (REST, PARACETAMOL).",
            "🟢"
        )
    
    # Default catch-all
    return (
        "YELLOW",
        "INCONCLUSIVE RESPONSE. PATIENT DEMANDS CLINICAL RE-ASSESSMENT. DISPENSE OTC REMEDIES AND REVIEW.",
        "🟡"
    )
