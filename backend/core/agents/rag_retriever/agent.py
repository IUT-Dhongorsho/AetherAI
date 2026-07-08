import os
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from backend.core.graph.state import PatientState

# === Load the same embedding model used in build_index.py ===
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return _model

from backend.rag.loader import load_vector_store

def load_index():
    """Load FAISS index and metadata from disk using the shared RAG loader."""
    index, metadata = load_vector_store()
    if index is not None and index.ntotal == 0 and len(metadata) == 0:
        return None, []
    return index, metadata

def rag_retriever(state: PatientState) -> PatientState:
    """
    Agent 4: RAG Retriever
    Uses FAISS to retrieve relevant clinical guidelines based on patient context.
    """
    state["retrieved_docs"] = []
    
    index, metadata = load_index()
    
    if index is None or index.ntotal == 0:
        state["retrieved_docs"] = [{
            "title": "Default Guidelines",
            "snippet": "If cough >14 days with fever, suspect Tuberculosis. If wheezing, suspect Asthma/COPD."
        }]
        return state

    # Formulate search query from state
    history = state.get("patient_history", {})
    transcript = state.get("transcript", "")
    prediction = state.get("audio_prediction", {})
    
    top_pred = max(prediction, key=prediction.get) if prediction else ""
    query = f"Patient has symptoms: {history}. Audio suggests {top_pred}. Transcript: {transcript}"
    
    # Use local embedding model (NO API call!)
    model = get_embedding_model()
    query_emb = model.encode([query]).astype('float32')
    
    k = min(3, index.ntotal)
    distances, indices = index.search(query_emb, k)
    
    docs = []
    for idx in indices[0]:
        if idx != -1 and idx < len(metadata):
            doc = metadata[idx]
            docs.append({
                "title": doc.get("title", "Unknown Source"),
                "snippet": doc.get("text", "")[:500]
            })
            
    if not docs:
        docs = [{
            "title": "Default Guidelines",
            "snippet": "If cough >14 days with fever, suspect Tuberculosis. If wheezing, suspect Asthma/COPD."
        }]
        
    state["retrieved_docs"] = docs
    return state
