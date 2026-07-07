import json
from google import genai
from google.genai import types
from backend.config import settings
from backend.core.graph.state import PatientState
from backend.core.agents.diagnosis_agent.schemas import DiagnosisResult

def diagnosis_agent(state: PatientState) -> PatientState:
    """
    Agent 5: Diagnosis & Triage Agent
    Fuses the outputs from previous agents and uses Gemini to generate a clinical recommendation.
    """
    if not settings.GEMINI_API_KEY:
        # Fallback if API key is not configured
        state["diagnosis"] = {"primary": "API Key Missing", "confidence": 0.0}
        state["triage_level"] = "UNKNOWN"
        state["action_text"] = "Please provide GEMINI_API_KEY in .env to get a real diagnosis."
        state["citations"] = []
        return state

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    # Construct the prompt context from state
    context = {
        "pharmacist_notes": state.get("pharmacist_notes", ""),
        "patient_history": state.get("patient_history", {}),
        "audio_prediction": state.get("audio_prediction", {}),
        "transcript": state.get("transcript", ""),
        "nlp_features": state.get("nlp_features", {}),
        "retrieved_docs": state.get("retrieved_docs", [])
    }
    
    prompt = f"""
    You are an expert clinical triage AI for a rural pharmacy. 
    Review the following patient data and RAG guidelines.
    
    PATIENT DATA:
    {json.dumps(context, indent=2)}
    
    RAG GUIDELINES:
    {json.dumps(state.get("retrieved_docs", []), indent=2)}
    
    OUTPUT:
    Return a response that strictly adheres to the provided schema.
    """

    print("⏳ Diagnosis Agent: Contacting Gemini 3.5 Flash API (this may take a moment if Google's servers are busy...)")
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DiagnosisResult,
                temperature=0.2,
            )
        )
        
        result = json.loads(response.text)
        state["diagnosis"] = {
            "primary": result.get("primary_diagnosis", "Unknown"),
            "confidence": float(result.get("confidence", 0.0))
        }
        state["triage_level"] = result.get("triage_level", "YELLOW")
        state["action_text"] = result.get("action_text", "")
        state["citations"] = result.get("citations", [])
        
    except Exception as e:
        print(f"⚠️ LLM API Error: {e}")
        state["diagnosis"] = {"primary": "Service Unavailable", "confidence": 0.0}
        state["triage_level"] = "YELLOW"
        state["action_text"] = f"The AI analysis service is currently unavailable. Error details: {str(e)}. Please try again later."
        state["citations"] = []
        
    return state
