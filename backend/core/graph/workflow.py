"""
LangGraph Workflow Engine - AetherAI
Orchestrates the 5 specialized agents in sequence.
"""

from langgraph.graph import StateGraph, END
from backend.core.graph.state import PatientState

# === Import the 5 agent functions (following the interfaces.py contract) ===
# NOTE: These functions are built by your teammate in /backend/core/agents/{agent_name}/agent.py
# We import them via the interfaces.py file to ensure type safety.
from backend.core.agents.interfaces import (
    intake_agent,
    audio_analyst,
    symptom_classifier,
    rag_retriever,
    diagnosis_agent
)

# === Build the Workflow ===
def build_workflow() -> StateGraph:
    """
    Creates and compiles the LangGraph workflow.
    Flow: Intake -> Audio -> NLP -> RAG -> Diagnosis -> END
    """
    
    # 1. Initialize the graph with the PatientState schema
    workflow = StateGraph(PatientState)
    
    # 2. Add the 5 nodes (Agents)
    workflow.add_node("intake_agent", intake_agent)           # Agent 1
    workflow.add_node("audio_analyst", audio_analyst)         # Agent 2
    workflow.add_node("symptom_classifier", symptom_classifier) # Agent 3
    workflow.add_node("rag_retriever", rag_retriever)         # Agent 4
    workflow.add_node("diagnosis_agent", diagnosis_agent)     # Agent 5
    
    # 3. Define the edges (The "Flow")
    workflow.set_entry_point("intake_agent")
    
    workflow.add_edge("intake_agent", "audio_analyst")
    workflow.add_edge("audio_analyst", "symptom_classifier")
    workflow.add_edge("symptom_classifier", "rag_retriever")
    workflow.add_edge("rag_retriever", "diagnosis_agent")
    
    # 4. End the workflow
    workflow.add_edge("diagnosis_agent", END)
    
    # 5. Compile the graph
    # (Note: checkpointer is optional for our hackathon, we can add it later)
    compiled = workflow.compile()
    
    return compiled

# === Singleton instance for FastAPI to import ===
app_graph = build_workflow()

# === (Optional) Quick test function to test the graph locally ===
if __name__ == "__main__":
    # This runs if you execute `python -m backend.core.graph.workflow`
    print("🔥 Testing AetherAI Workflow locally...")
    
    # Mock initial state (without any agent outputs yet)
    initial_state: PatientState = {
        "patient_id": "test_001",
        "audio_path": "data/sample_audio/cough.wav",
        "pharmacist_notes": "Patient has fever and cough for 2 weeks"
    }
    
    # Invoke the graph
    result = app_graph.invoke(initial_state)
    
    # Print the final triage
    print(f"Triage Level: {result.get('triage_level')}")
    print(f"Action: {result.get('action_text')}")
    print(f"Diagnosis: {result.get('diagnosis')}")
    print("✅ Graph test executed successfully!")
