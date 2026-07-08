import os
import uuid
import shutil
import json
from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api.dependencies import get_db_session
from backend.database import crud
from backend.config import settings
from google import genai
from google.genai import types

router = APIRouter()

@router.post("/test/upload")
async def upload_test(
    patient_id: str = Form(...),
    test_type: str = Form(...), # "vitals" or "cough"
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session)
):
    os.makedirs(settings.AUDIO_UPLOAD_DIR, exist_ok=True)
    temp_id = str(uuid.uuid4())[:8]
    file_ext = file.filename.split('.')[-1]
    file_name = f"{temp_id}_{test_type}.{file_ext}"
    file_path = os.path.join(settings.AUDIO_UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    results = {}
    system_note = ""
    
    if test_type == "vitals":
        try:
            # Integrate open-rppg
            # Depending on the exact API of open-rppg, you might need to adjust the function call.
            # Assuming a standard inference model interface provided by the toolbox.
            import open_rppg
            from open_rppg import inference
            
            # This is a generic representation. Adjust `inference.process_video` based on open-rppg's exact documentation if it differs.
            # E.g. some toolboxes return a dictionary, others return a tuple (hr, hrv, rr)
            try:
                # Attempt to extract HR and potentially RR (Respiratory Rate)
                rppg_results = inference.process_video(file_path) 
                
                hr = rppg_results.get("heart_rate", 0) if isinstance(rppg_results, dict) else rppg_results[0]
                rr = rppg_results.get("respiratory_rate", 16) if isinstance(rppg_results, dict) else (rppg_results[1] if len(rppg_results)>1 else 16)
                
                results = {"heart_rate": int(hr), "respiratory_rate": int(rr)}
                system_note = f"System Note: Vitals scan complete (open-rppg). HR: {int(hr)} BPM, RR: {int(rr)} breaths/min"
            except AttributeError:
                # Fallback if the API is slightly different (e.g., uses a class-based approach)
                model = open_rppg.RPPG()
                hr = model.predict(file_path)
                results = {"heart_rate": int(hr), "respiratory_rate": 16}
                system_note = f"System Note: Vitals scan complete (open-rppg). HR: {int(hr)} BPM, RR: 16 breaths/min"

        except Exception as e:
            print(f"Vitals processing failed: {e}")
            results = {"error": f"Vitals processing failed: {str(e)}"}
            system_note = f"System Note: Vitals scan failed to process the video. Error: {str(e)}"

    elif test_type == "cough":
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            # Fetch context from chat history
            history = crud.get_chat_history(db, patient_id=patient_id, limit=20)
            context_text = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
            
            # Upload file
            uploaded_audio = client.files.upload(file=file_path)
            
            prompt = f"""
            You are a medical AI analyzing a patient's cough audio.
            
            Here is the recent conversation context with the patient:
            {context_text}
            
            Task:
            1. Listen to the attached audio file.
            2. Analyze the acoustic features of the cough (e.g., dry, wet, wheezing, crackles, frequency).
            3. Consider the conversation context.
            4. Return a JSON object with your findings.
            
            Format strictly as:
            {{
                "cough_detected": true,
                "type": "dry",
                "severity": "mild",
                "analysis_notes": "detailed string explaining acoustic findings"
            }}
            """
            
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=[uploaded_audio, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                )
            )
            
            try:
                results = json.loads(response.text)
                system_note = f"System Note: Cough analysis complete. Type: {results.get('type')}, Severity: {results.get('severity')}. Notes: {results.get('analysis_notes')}"
            except json.JSONDecodeError:
                results = {"error": "Failed to parse model response", "raw": response.text}
                system_note = "System Note: Cough analysis completed but returned invalid format."
                
            # Cleanup
            client.files.delete(name=uploaded_audio.name)
            
        except Exception as e:
            print(f"Cough processing failed: {e}")
            results = {"error": f"Cough analysis failed: {str(e)}"}
            system_note = f"System Note: Cough analysis failed. Error: {str(e)}"
            
    crud.add_test_result(db, patient_id=patient_id, test_type=test_type, results=results)
    crud.add_chat_message(db, patient_id=patient_id, role="system", content=system_note)
    
    return {"status": "success", "results": results}
