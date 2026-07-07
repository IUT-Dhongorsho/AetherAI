import os
import torch
from torchvision.models import resnet50, ResNet50_Weights
from transformers import pipeline

# Set the cache directory to the local 'weights' folder
weights_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "weights"))
os.makedirs(weights_dir, exist_ok=True)
os.environ["HF_HOME"] = weights_dir
os.environ["TORCH_HOME"] = weights_dir

print(f"Downloading all models to: {weights_dir}\n")

print("1/3: Downloading ResNet50 for Audio...")
resnet50(weights=ResNet50_Weights.DEFAULT)
print("✅ ResNet50 Downloaded!\n")

print("2/3: Downloading Whisper (Tiny) for Speech-to-Text...")
pipeline("automatic-speech-recognition", model="openai/whisper-tiny")
print("✅ Whisper Downloaded!\n")

print("3/3: Downloading BERT for NER...")
# We use a much smaller model (~400MB) instead of the massive 2.2GB one
pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print("✅ NER Model Downloaded!\n")

print("🎉 All weights successfully downloaded to the local directory!")
