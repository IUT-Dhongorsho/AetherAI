# 🩺 AetherAI - The AI Pharmacist's Stethoscope

AetherAI is a **Multi-Agent AI Triage System** designed to aid rural pharmacists and community health workers in Bangladesh. By analyzing a patient's symptoms and cough audio recording, it screens for major respiratory conditions (Normal, Pneumonia, Tuberculosis, Asthma, and COPD) and provides color-coded, actionable recommendations (**Red / Yellow / Green Alerts**).

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- SQLite3

### 2. Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourteam/aetherai.git
   cd aetherai
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory (see `.env.example`):
   ```ini
   GEMINI_API_KEY=your_google_gemini_api_key_here
   DATABASE_URL=sqlite:///./aetherai.db
   AUDIO_UPLOAD_DIR=./uploads
   HF_TOKEN=your_huggingface_token_here (optional, for higher rate limits)
   ```

   > [!NOTE]
   > **How to get a Google Gemini API Key:**
   > 1. Visit the [Google AI Studio](https://aistudio.google.com/).
   > 2. Log in with your Google account.
   > 3. Click **"Get API Key"** and create a new key. It is free for standard testing!

5. **Initialize RAG Index:**
   Place the medical guidelines PDFs (like WHO Pneumonia guidelines or Bangladesh NTP guidelines) inside `backend/rag/documents/` and run the indexing script:
   ```bash
   python backend/rag/build_index.py
   ```
   *Note: If no PDFs are present, a dummy index will automatically be generated to prevent startup crashes.*

### 3. Running the Backend Server
```bash
uvicorn backend.main:app --reload
```
The API docs will be accessible at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧬 System Architecture & Technological Flow

The system runs a strictly linear multi-agent workflow orchestrated sequentially:

1.  **Intake Agent**: Collects demographic details and extracts clinical symptoms (fever, weight loss, cough duration) from the pharmacist's notes.
2.  **Audio Analyst**: Queries the Hugging Face Inference API to analyze the cough recording, returning predicted probabilities for Normal, Pneumonia, Tuberculosis, Asthma, and COPD.
3.  **Symptom Classifier**: Transcribes the audio recording using **Whisper** and extracts clinical terms using **BERT NER** via the Hugging Face Inference API.
4.  **RAG Retriever**: Creates semantic embeddings of the context and queries a local **FAISS Vector Database** containing national guidelines for relevant triage protocols.
5.  **Diagnosis Agent**: Fuses the multi-agent findings using **Gemini 3.5 Flash** to compile a final diagnosis, triage alert rating, and action instructions.

### 🛡️ Safety Net Fallback
If the LLM or external APIs fail, a **Deterministic Fallback Triage Service** evaluates the acoustic scores and symptoms directly (e.g. *crackles > 0.70 + fever + cough duration >= 14 days* $\rightarrow$ **RED ALERT / Refer for GeneXpert TB Testing**) to ensure the API remains operational and safe.
