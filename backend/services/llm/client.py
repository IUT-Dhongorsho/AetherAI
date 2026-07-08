from google import genai
from backend.config import settings

# Unified LLM client for Google Gemini
if settings.GEMINI_API_KEY:
    try:
        llm_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        print(f"Error initializing GenAI Client: {e}")
        llm_client = None
else:
    llm_client = None
