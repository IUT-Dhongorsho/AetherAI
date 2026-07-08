import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API
    API_VERSION = "v1"
    PROJECT_NAME = "AetherAI"
    
    # LLM
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aetherai.db")
    
    # Uploads
    AUDIO_UPLOAD_DIR = os.getenv("AUDIO_UPLOAD_DIR", "./uploads")
    
    # CORS
    ALLOWED_ORIGINS = ["*"]  # For hackathon, lock down in production

settings = Settings()
