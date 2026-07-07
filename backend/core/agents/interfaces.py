"""
THE GOLDEN CONTRACT - With partial implementations.
Agents that are ready are imported; others remain mocked.
"""

from typing import Dict, Any, Callable, TypedDict, List, Optional
from backend.core.graph.state import PatientState

# Import actual implemented agents
from backend.core.agents.intake_agent.agent import intake_agent
from backend.core.agents.diagnosis_agent.agent import diagnosis_agent

from backend.core.agents.audio_analyst.agent import audio_analyst

AgentFunction = Callable[[PatientState], PatientState]

from backend.core.agents.symptom_classifier.agent import symptom_classifier

from backend.core.agents.rag_retriever.agent import rag_retriever

# All agents are now fully imported and implemented.
