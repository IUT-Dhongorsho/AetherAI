import os
import faiss
import numpy as np
from pypdf import PdfReader
from google import genai
from google.genai import types
from backend.core.graph.state import PatientState
from backend.config import settings

DOCS_DIR = "backend/rag/documents"
INDEX_PATH = "backend/rag/vector_store/faiss_index.bin"
METADATA_PATH = "backend/rag/vector_store/metadata.npy"

# Cached globals
_index = None
_metadata = None
_client = None

def get_genai_client():
    global _client
    if _client is None and settings.GEMINI_API_KEY:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client

def embed_text(text: str) -> np.ndarray:
    client = get_genai_client()
    if not client:
        # Fallback to random if no API key
        return np.random.rand(768).astype('float32')
        
    try:
        response = client.models.embed_content(
            model="text-embedding-004",
            contents=text
        )
        return np.array(response.embeddings[0].values, dtype=np.float32)
    except Exception as e:
        print(f"Embedding error: {e}")
        return np.random.rand(768).astype('float32')

def load_index():
    global _index, _metadata
    if _index is None:
        if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
            _index = faiss.read_index(INDEX_PATH)
            _metadata = np.load(METADATA_PATH, allow_pickle=True)
        else:
            # If not built, just create an empty one with dim 768
            _index = faiss.IndexFlatL2(768)
            _metadata = np.array([])
    return _index, _metadata

def rag_retriever(state: PatientState) -> PatientState:
    """
    Agent 4: RAG Retriever
    Uses FAISS to retrieve relevant clinical guidelines based on patient context.
    """
    state["retrieved_docs"] = []
    
    index, metadata = load_index()
    if index.ntotal == 0:
        # Return fallback guidelines if RAG isn't built yet
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
    
    query_emb = embed_text(query).reshape(1, -1)
    
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
