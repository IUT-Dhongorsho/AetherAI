import os
import pickle
import numpy as np
import faiss
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

DOCS_DIR = "backend/rag/documents"
VECTOR_STORE_DIR = "backend/rag/vector_store"
INDEX_PATH = os.path.join(VECTOR_STORE_DIR, "faiss_index.bin")
METADATA_PATH = os.path.join(VECTOR_STORE_DIR, "metadata.pkl")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """Splits text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def build_vector_store():
    print("🚀 Starting RAG Ingestion (Pure Python, No LangChain)...")
    
    # Ensure directories exist
    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    
    pdf_files = [f for f in os.listdir(DOCS_DIR) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"⚠️ No PDFs found in '{DOCS_DIR}'. Skipping RAG build.")
        return

    print(f"📄 Found {len(pdf_files)} PDF(s). Extracting text...")
    all_chunks = []
    metadata = []  # Stores (filename, chunk_text)

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
                metadata.append({"title": file_name, "text": chunk})
            print(f"  ✅ Extracted {len(chunks)} chunks from {file_name}")
        except Exception as e:
            print(f"  ❌ Failed to read {file_name}: {e}")

    if not all_chunks:
        print("⚠️ No text extracted. Exiting.")
        return

    # Step 2: Load a small, fast local embedding model
    print(f"🧠 Loading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    print(f"🧠 Generating embeddings for {len(all_chunks)} chunks...")
    # Batch encode for speed
    embeddings = model.encode(all_chunks, show_progress_bar=True)
    
    # Convert to float32 for FAISS
    embeddings = np.array(embeddings).astype('float32')
    
    # Step 3: Build FAISS index
    print("💾 Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Save index and metadata
    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, 'wb') as f:
        pickle.dump(metadata, f)
    
    print(f"✅ RAG index built successfully with {len(all_chunks)} chunks!")
    print(f"📂 Saved to: {INDEX_PATH} and {METADATA_PATH}")

if __name__ == "__main__":
    build_vector_store()
