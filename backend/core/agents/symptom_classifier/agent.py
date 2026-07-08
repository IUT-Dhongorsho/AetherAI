import os
from huggingface_hub import InferenceClient
from backend.core.graph.state import PatientState

def symptom_classifier(state: PatientState) -> PatientState:
    """
    Agent 3: Symptom Classifier
    Transcribes the audio using Hugging Face Whisper Inference API and extracts symptoms.
    """
    audio_path = state.get("audio_path")
    
    # 1. Transcription (STT) via Hugging Face Inference Client
    transcript = ""
    if audio_path and os.path.exists(audio_path):
        try:
            token = os.getenv("HF_TOKEN", None)
            client = InferenceClient(token=token)
            
            # Use Whisper on HF Inference API
            with open(audio_path, "rb") as f:
                audio_data = f.read()
                
            # Call HF Inference API for automatic speech recognition
            response = client.automatic_speech_recognition(
                audio_data, 
                model="openai/whisper-large-v3-turbo"
            )
            transcript = response.text if hasattr(response, 'text') else str(response)
        except Exception as e:
            print(f"STT HF API Error: {e}")
            # Fallback to pharmacist notes
            notes = state.get("pharmacist_notes", "")
            transcript = notes if notes else f"[Transcription failed: {e}]"
            
    state["transcript"] = transcript
    
    # 2. Symptom Extraction (NER / Keyphrase detection) via HF or local string heuristics
    entities = []
    if transcript:
        try:
            token = os.getenv("HF_TOKEN", None)
            client = InferenceClient(token=token)
            
            # Query NER model on HF Inference API
            ner_results = client.token_classification(
                transcript, 
                model="dslim/bert-base-NER"
            )
            for ent in ner_results:
                if isinstance(ent, dict):
                    word = ent.get("word", "")
                else:
                    word = getattr(ent, "word", "")
                if word:
                    entities.append(word)
        except Exception as e:
            print(f"NER HF API Error: {e}")
            # Fallback: Simple keyword extraction for common symptoms in Bangladesh context
            common_symptoms = ["fever", "cough", "weight loss", "chest pain", "breathing", "wheezing", "asthma", "tb", "sputum", "blood"]
            for symptom in common_symptoms:
                if symptom in transcript.lower():
                    entities.append(symptom)
                    
    state["nlp_features"] = {
        "entities": list(set(entities)),
        "distress_level": "moderate"
    }
    
    return state