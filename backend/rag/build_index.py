import os
import faiss
import numpy as np
from pypdf import PdfReader
from google import genai
from dotenv import load_dotenv

# Ensure we load environment variables if run as a standalone script
load_dotenv()

# We can import settings from our config
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.config import settings

DOCS_DIR = "backend/rag/documents"
VECTOR_STORE_DIR = "backend/rag/vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_index.bin")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.npy")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """Splits text into smaller overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def build_index():
    print("🚀 Starting Phase 1: RAG Ingestion...")
    
    if not settings.GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY is not set in .env")
        return
        
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    
    if not os.path.exists(VECTOR_STORE_DIR):
        os.makedirs(VECTOR_STORE_DIR)
        
    pdf_files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.pdf')]
    
    if not pdf_files:
        print(f"⚠️ No PDF files found in '{DOCS_DIR}'.")
        print("Please place your clinical guidelines (WHO/NTP PDFs) in that folder and run this script again.")
        # Create a dummy metadata/index so the app doesn't crash, but it won't have real data.
        dummy_index = faiss.IndexFlatL2(768)
        faiss.write_index(dummy_index, INDEX_PATH)
        np.save(METADATA_PATH, np.array([]))
        return

    all_chunks = []
    metadata = []
    
    print(f"📄 Found {len(pdf_files)} PDF(s). Extracting text...")
    for file_name in pdf_files:
        file_path = os.path.join(DOCS_DIR, file_name)
        try:
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            
            chunks = chunk_text(full_text)
            for chunk in chunks:
                all_chunks.append(chunk)
                metadata.append({
                    "title": file_name,
                    "text": chunk
                })
        except Exception as e:
            print(f"❌ Failed to read {file_name}: {e}")

    if not all_chunks:
        print("⚠️ No text could be extracted from the PDFs.")
        return

    print(f"🧠 Generating embeddings for {len(all_chunks)} chunks using Gemini...")
    embeddings = []
    
    for i, chunk in enumerate(all_chunks):
        try:
            # Using the embedding model
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=chunk
            )
            embeddings.append(response.embeddings[0].values)
            print(f"  [{i+1}/{len(all_chunks)}] Embedded chunk")
        except Exception as e:
            print(f"❌ Failed to embed chunk {i}: {e}")
            # Append zeros as fallback for failed chunks to maintain alignment
            embeddings.append([0.0] * 768)

    print("💾 Building FAISS Index...")
    # Convert list to numpy array of float32
    embeddings_matrix = np.array(embeddings).astype('float32')
    
    # Text-embedding-004 dimension is 768
    dimension = 768 
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_matrix)
    
    # Save the index and metadata
    faiss.write_index(index, INDEX_PATH)
    np.save(METADATA_PATH, np.array(metadata, dtype=object))
    
    print(f"✅ Success! RAG database built with {len(all_chunks)} chunks.")
    print(f"📂 Saved to: {INDEX_PATH} and {METADATA_PATH}")

if __name__ == "__main__":
    build_index()
