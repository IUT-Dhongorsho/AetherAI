from backend.core.graph.state import PatientState

def intake_agent(state: PatientState) -> PatientState:
    """
    Agent 1: Intake Agent
    Collects patient history and context. For now, it simply parses the initial
    input and structure the patient_history dict.
    """
    # patient_history is initialized in predict.py, so we just ensure it exists
    # and maybe process any natural language pharmacist_notes if needed later.
    if "patient_history" not in state:
        state["patient_history"] = {}
        
    # Example logic: extract keywords from notes to populate history (mocked logic for now)
    notes = state.get("pharmacist_notes", "").lower()
    if "fever" in notes:
        state["patient_history"]["fever"] = True
    if "weight loss" in notes or "weightloss" in notes:
        state["patient_history"]["weight_loss"] = True
        
    # Extract duration of cough in days if specified (e.g. "15 days", "2 weeks")
    import re
    duration_match = re.search(r'(\d+)\s*day', notes)
    if duration_match:
        state["patient_history"]["duration_days"] = int(duration_match.group(1))
    else:
        weeks_match = re.search(r'(\d+)\s*week', notes)
        if weeks_match:
            state["patient_history"]["duration_days"] = int(weeks_match.group(1)) * 7
        
    return state
