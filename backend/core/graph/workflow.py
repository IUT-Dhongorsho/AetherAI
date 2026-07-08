from backend.core.graph.state import PatientState
from backend.core.agents.interfaces import (
    intake_agent, audio_analyst, symptom_classifier,
    rag_retriever, diagnosis_agent
)

def run_pipeline(initial_state: dict) -> dict:
    """
    Runs the 5-agent clinical triage pipeline sequentially.
    intake_agent → audio_analyst → symptom_classifier → rag_retriever → diagnosis_agent
    PatientState is a TypedDict (plain dict at runtime) — just copy directly.
    """
    state: PatientState = dict(initial_state)  # type: ignore[assignment]
    
    # 1. Intake Agent
    state = intake_agent(state)
    
    # 2. Audio Analyst
    state = audio_analyst(state)
    
    # 3. Symptom Classifier
    state = symptom_classifier(state)
    
    # 4. RAG Retriever
    state = rag_retriever(state)
    
    # 5. Diagnosis Agent
    state = diagnosis_agent(state)
    
    return state

class SequentialPipeline:
    def invoke(self, initial_state: dict) -> dict:
        return run_pipeline(initial_state)

# Keep the variable name app_graph so predict.py doesn't break
app_graph = SequentialPipeline()
