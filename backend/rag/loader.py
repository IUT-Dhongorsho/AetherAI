import os
import faiss
import pickle

# Resolve paths relative to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INDEX_PATH = os.path.join(BASE_DIR, "backend", "rag", "vector_store", "faiss_index.bin")
METADATA_PATH = os.path.join(BASE_DIR, "backend", "rag", "vector_store", "metadata.pkl")

def load_vector_store():
    """
    Loads and returns the FAISS index and metadata for RAG retrieval.
    If the index files do not exist, returns an empty IndexFlatL2 (dim 384) and empty list.
    Note: sentence-transformers/all-MiniLM-L6-v2 produces 384-dimensional embeddings.
    """
    if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
        try:
            index = faiss.read_index(INDEX_PATH)
            with open(METADATA_PATH, 'rb') as f:
                metadata = pickle.load(f)
            return index, metadata
        except Exception as e:
            print(f"Error loading FAISS vector store: {e}")
            
    # Fallback to empty index (MiniLM dimension is 384)
    index = faiss.IndexFlatL2(384)
    metadata = []
    return index, metadata
