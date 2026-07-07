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
    if "weight loss" in notes:
        state["patient_history"]["weight_loss"] = True
        
    return state
