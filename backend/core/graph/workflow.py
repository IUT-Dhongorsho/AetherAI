from langgraph.graph import StateGraph, END
from backend.core.graph.state import PatientState
from backend.core.agents.interfaces import (
    intake_agent, audio_analyst, symptom_classifier,
    rag_retriever, diagnosis_agent
)

def build_workflow():
    workflow = StateGraph(PatientState)
    
    workflow.add_node("intake_agent", intake_agent)
    workflow.add_node("audio_analyst", audio_analyst)
    workflow.add_node("symptom_classifier", symptom_classifier)
    workflow.add_node("rag_retriever", rag_retriever)
    workflow.add_node("diagnosis_agent", diagnosis_agent)
    
    workflow.set_entry_point("intake_agent")
    workflow.add_edge("intake_agent", "audio_analyst")
    workflow.add_edge("audio_analyst", "symptom_classifier")
    workflow.add_edge("symptom_classifier", "rag_retriever")
    workflow.add_edge("rag_retriever", "diagnosis_agent")
    workflow.add_edge("diagnosis_agent", END)
    
    return workflow.compile()

app_graph = build_workflow()
