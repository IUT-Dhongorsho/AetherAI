import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

try:
    print("calling gemini")
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents="Hello",
    )
    print("response:", response.text)
except Exception as e:
    print("error:", e)
