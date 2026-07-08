import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid

def generate_cough_graph_image(audio_path: str, output_dir: str = "reports") -> str:
    """
    Reads an audio file, generates a Mel-Spectrogram, saves it as a PNG,
    and returns the file path to the saved image.
    """
    os.makedirs(output_dir, exist_ok=True)
    image_name = f"spectrogram_{uuid.uuid4().hex[:8]}.png"
    output_path = os.path.join(output_dir, image_name)

    try:
        y, sr = librosa.load(audio_path, sr=16000)
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mel_spec_db, sr=sr, x_axis='time', y_axis='mel', cmap='magma')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Cough Analysis (Mel-Spectrogram)')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return output_path
    except Exception as e:
        print(f"Failed to generate cough graph: {e}")
        return ""
