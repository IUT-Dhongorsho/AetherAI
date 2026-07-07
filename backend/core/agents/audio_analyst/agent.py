import os
import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
from backend.core.graph.state import PatientState
from backend.core.agents.audio_analyst.preprocess import extract_mel_spectrogram

# Define the 5 respiratory conditions
CLASSES = ["Normal", "Pneumonia", "Tuberculosis", "Asthma", "COPD"]

# Global model initialization to avoid reloading on every request
_model = None
MODEL_PATH = "backend/core/models/audio_model.pth"

def get_audio_model():
    global _model
    if _model is None:
        # Load ResNet50
        _model = resnet50(weights=ResNet50_Weights.DEFAULT)
        # Modify the final classification layer for 5 classes
        num_ftrs = _model.fc.in_features
        _model.fc = nn.Linear(num_ftrs, len(CLASSES))
        
        # Try loading fine-tuned weights if they exist
        if os.path.exists(MODEL_PATH):
            try:
                _model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
                print(f"Loaded audio model weights from {MODEL_PATH}")
            except Exception as e:
                print(f"Failed to load weights: {e}")
                
        _model.eval()
    return _model

def audio_analyst(state: PatientState) -> PatientState:
    """
    Agent 2: Audio Analyst
    Takes the audio_path, extracts the Mel-Spectrogram, and passes it through ResNet50
    to predict respiratory conditions.
    """
    audio_path = state.get("audio_path")
    if not audio_path or not os.path.exists(audio_path):
        state["audio_prediction"] = {"Error": 1.0}
        state["audio_features"] = {"status": "Missing audio file"}
        return state

    try:
        # 1. Preprocess
        input_tensor = extract_mel_spectrogram(audio_path)
        
        # 2. Inference
        model = get_audio_model()
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
        # 3. Format output mapping classes to probabilities
        predictions = {
            CLASSES[i]: float(probabilities[i]) for i in range(len(CLASSES))
        }
        
        state["audio_prediction"] = predictions
        state["audio_features"] = {"sample_rate": 16000, "status": "Success"}
        
    except Exception as e:
        state["audio_prediction"] = {"Error": 1.0}
        state["audio_features"] = {"status": f"Failed processing: {str(e)}"}

    return state
