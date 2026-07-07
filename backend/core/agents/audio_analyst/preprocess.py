import librosa
import numpy as np
import torch
from torchvision import transforms

def extract_mel_spectrogram(audio_path: str, sr: int = 16000, n_mels: int = 128, max_len: int = 150) -> torch.Tensor:
    """
    Extracts a Mel-spectrogram from an audio file and converts it into a format
    suitable for ResNet50 (3 channels, normalized).
    """
    # 1. Load audio
    y, _ = librosa.load(audio_path, sr=sr)
    
    # 2. Extract Mel-spectrogram
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
    
    # 3. Pad or truncate to max_len (e.g., 5 seconds)
    if mel_spec_db.shape[1] < max_len:
        pad_width = max_len - mel_spec_db.shape[1]
        mel_spec_db = np.pad(mel_spec_db, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mel_spec_db = mel_spec_db[:, :max_len]
        
    # 4. Normalize to [0, 1]
    mel_spec_db = (mel_spec_db - mel_spec_db.min()) / (mel_spec_db.max() - mel_spec_db.min() + 1e-6)
    
    # 5. Convert to PyTorch tensor (C, H, W) -> ResNet expects 3 channels
    tensor_spec = torch.tensor(mel_spec_db, dtype=torch.float32).unsqueeze(0) # (1, H, W)
    tensor_spec = tensor_spec.repeat(3, 1, 1) # (3, H, W)
    
    # Optional: Apply ImageNet normalization (often used with pre-trained ResNet)
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    tensor_spec = normalize(tensor_spec)
    
    return tensor_spec.unsqueeze(0) # Add batch dimension -> (1, 3, H, W)
