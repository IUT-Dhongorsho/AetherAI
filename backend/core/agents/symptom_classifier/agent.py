import os
from transformers import pipeline
from backend.core.graph.state import PatientState

# Globals to cache models
_stt_pipeline = None
_ner_pipeline = None

def get_stt_pipeline():
    global _stt_pipeline
    if _stt_pipeline is None:
        try:
            print("Loading Whisper STT model...")
            _stt_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")
        except Exception as e:
            print(f"Failed to load Whisper: {e}")
    return _stt_pipeline

def get_ner_pipeline():
    global _ner_pipeline
    if _ner_pipeline is None:
        try:
            print("Loading NER model...")
            # Using a much smaller NER model (dslim/bert-base-NER) instead of the 2.2GB xlm-roberta model
            _ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
        except Exception as e:
            print(f"Failed to load NER model: {e}")
    return _ner_pipeline

def symptom_classifier(state: PatientState) -> PatientState:
    """
    Agent 3: Symptom Classifier
    Transcribes the audio using Whisper and extracts symptoms via NER.
    """
    audio_path = state.get("audio_path")
    
    # 1. Transcription (STT)
    transcript = ""
    if audio_path and os.path.exists(audio_path):
        stt = get_stt_pipeline()
        if stt:
            try:
                # Transcribe
                result = stt(audio_path)
                transcript = result.get("text", "").strip()
            except Exception as e:
                print(f"STT Error: {e}")
                transcript = f"[Transcription failed: {e}]"
    
    state["transcript"] = transcript
    
    # 2. Symptom Extraction (NER)
    entities = []
    if transcript:
        ner = get_ner_pipeline()
        if ner:
            try:
                # Basic NER processing
                ner_results = ner(transcript)
                # Keep entities that are disease or symptom related (mocked by extracting words)
                for ent in ner_results:
                    # simplistic extraction for the prototype
                    entities.append(ent.get("word", ""))
            except Exception as e:
                print(f"NER Error: {e}")
                
    state["nlp_features"] = {
        "entities": entities,
        "distress_level": "moderate" # Could be computed based on speech rate or specific keywords
    }
    
    return state