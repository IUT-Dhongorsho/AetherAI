from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.api.dependencies import get_db_session
from backend.database import crud
from backend.config import settings
from google import genai
from google.genai import types

router = APIRouter()

class ChatRequest(BaseModel):
    patient_id: str
    message: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db_session)):
    # 1. Append user message to DB
    crud.add_chat_message(db, patient_id=request.patient_id, role="user", content=request.message)

    # 2. Get chat history
    history = crud.get_chat_history(db, patient_id=request.patient_id, limit=10)
    
    # Format for Gemini
    contents = []
    for msg in history:
        role = msg.role
        if role == "system":
            role = "user" # Gemini supports 'user' and 'model'
            
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg.content)]
            )
        )
        
    # 3. Call Gemini
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    tools = [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="trigger_cough_test",
                    description="Call this tool if the patient reports coughing, wheezing, or chest congestion. It will ask the patient to record a 5-second audio clip of their cough.",
                ),
                types.FunctionDeclaration(
                    name="trigger_vitals_test",
                    description="Call this tool to measure the patient's Heart Rate (BPM) and Respiratory Rate. It will ask the patient to look into their camera for 10 seconds.",
                ),
                types.FunctionDeclaration(
                    name="finalize_diagnosis",
                    description="Call this tool when you have collected enough conversational and sensor data to confidently diagnose the patient. Pass the final diagnosis and recommended medicines as arguments.",
                    parameters={
                        "type": "OBJECT",
                        "properties": {
                            "diagnosis": {"type": "STRING", "description": "The final diagnosis"},
                            "medicines": {
                                "type": "ARRAY", 
                                "items": {"type": "STRING"},
                                "description": "Recommended medicines"
                            }
                        },
                        "required": ["diagnosis", "medicines"]
                    }
                )
            ]
        )
    ]

    system_instruction = "You are AetherAI, an Event-Driven, Multi-Modal Conversational Diagnostic Agent. Converse with the patient naturally in English or Bangla to diagnose them. Use tools to gather sensor data when appropriate."

    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                tools=tools
            )
        )
        
        # Check if model called a tool
        if response.function_calls:
            fc = response.function_calls[0]
            if fc.name == "trigger_cough_test":
                return {"type": "tool_trigger", "action": "show_cough_card"}
            elif fc.name == "trigger_vitals_test":
                return {"type": "tool_trigger", "action": "show_vitals_card"}
            elif fc.name == "finalize_diagnosis":
                args = fc.args
                diagnosis = args.get("diagnosis", "")
                medicines = args.get("medicines", [])
                
                # Fetch full data for PDF
                full_history = crud.get_chat_history(db, patient_id=request.patient_id, limit=50)
                from backend.database.models import TestResult
                test_results = db.query(TestResult).filter(TestResult.patient_id == request.patient_id).all()
                
                from backend.services.reporting.service import generate_pdf_report
                pdf_path = generate_pdf_report(
                    patient_id=request.patient_id,
                    diagnosis=diagnosis,
                    medicines=medicines,
                    chat_history=full_history,
                    test_results=test_results
                )
                
                pdf_url = f"/reports/{os.path.basename(pdf_path)}"
                
                # Append system msg for diagnosis
                crud.add_chat_message(db, patient_id=request.patient_id, role="system", content=f"Diagnosis finalized: {diagnosis}")
                
                return {
                    "type": "tool_trigger", 
                    "action": "generate_prescription", 
                    "data": {
                        "diagnosis": diagnosis, 
                        "medicines": medicines, 
                        "pdf_url": pdf_url
                    }
                }
        
        # Regular text response
        reply_text = response.text
        crud.add_chat_message(db, patient_id=request.patient_id, role="model", content=reply_text)
        
        return {"type": "message", "content": reply_text}
        
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return {"type": "message", "content": f"System Error: Google Gemini API rejected the request. Details: {str(e)}"}
