import os
import httpx

def classify_audio_via_api(audio_path: str) -> dict:
    """
    Sends the audio file to a pre-built Hugging Face model via the Inference API
    that directly classifies ILLNESSES (e.g., Pneumonia, COVID-19, Asthma).
    """
    hf_token = os.getenv("HF_TOKEN")
    
    # You MUST replace this with the exact ID of the illness-classification model you find on Hugging Face!
    # Examples of datasets these models are trained on: ICBHI 2017, COUGHVID, etc.
    model_id = os.getenv("HF_MODEL_ID", "your-chosen-author/respiratory-illness-classifier")
    
    if not hf_token:
        print("⚠️ No HF_TOKEN found in .env. Falling back to a mock ILLNESS response so the app doesn't crash.")
        # Simulating a model that directly outputs illness probabilities
        return {"Pneumonia": 0.75, "Asthma": 0.15, "Normal": 0.10}

    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    print(f"📡 Sending {os.path.basename(audio_path)} to Hugging Face Illness API ({model_id})...")
    
    try:
        with open(audio_path, "rb") as f:
            data = f.read()
            
        response = httpx.post(url, headers=headers, content=data, timeout=30.0)
        
        if response.status_code == 200:
            results = response.json()
            
            # Convert list to a simple dictionary {illness_label: score}
            predictions = {}
            if isinstance(results, list):
                for item in results[:5]:  
                    predictions[item.get("label", "Unknown_Illness")] = round(item.get("score", 0.0), 3)
                return predictions
            return {"Raw_Response": results}
            
        elif response.status_code == 503:
            print("⚠️ Hugging Face model is waking up (503). It usually takes 20 seconds. Try again.")
            return {"Status": "Model Loading on Hugging Face."}
        else:
            print(f"⚠️ Hugging Face API error {response.status_code}: {response.text}")
            return {"Error": response.text}
            
    except httpx.RequestError as e:
        print(f"⚠️ Failed to connect to Hugging Face: {e}")
        return {"Error": str(e)}
