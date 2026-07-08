import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from datetime import datetime

def generate_pdf_report(patient_id: str, diagnosis: str, medicines: list, chat_history: list, test_results: list):
    os.makedirs("reports", exist_ok=True)
    file_name = f"aetherai_prescription_{patient_id}.pdf"
    file_path = os.path.join("reports", file_name)
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, height - 1*inch, "AetherAI Medical Prescription")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 1.3*inch, f"Patient ID: {patient_id}")
    c.drawString(1*inch, height - 1.5*inch, f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC")
    
    # Diagnosis
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 2*inch, "Final Diagnosis:")
    c.setFont("Helvetica", 12)
    
    y_pos = height - 2.3*inch
    c.drawString(1*inch, y_pos, diagnosis)
    y_pos -= 0.5*inch
    
    # Medicines
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_pos, "Recommended Medicines:")
    y_pos -= 0.3*inch
    c.setFont("Helvetica", 12)
    for med in medicines:
        c.drawString(1*inch, y_pos, f"• {med}")
        y_pos -= 0.2*inch
        
    y_pos -= 0.3*inch
    
    # Test Results
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_pos, "Sensor Test Data:")
    y_pos -= 0.3*inch
    c.setFont("Helvetica", 12)
    for test in test_results:
        c.drawString(1*inch, y_pos, f"• {test.test_type.upper()}: {test.results}")
        y_pos -= 0.2*inch
        
    y_pos -= 0.3*inch
    
    # Conversation Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y_pos, "Key Patient Symptoms (From Chat):")
    y_pos -= 0.3*inch
    c.setFont("Helvetica", 10)
    
    user_messages = [msg for msg in chat_history if msg.role == 'user']
    for msg in user_messages[-5:]: # Last 5 messages
        content = (msg.content[:80] + '...') if len(msg.content) > 80 else msg.content
        c.drawString(1*inch, y_pos, f"- {content}")
        y_pos -= 0.2*inch
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(1*inch, 0.5*inch, "This is an AI-generated prescription. Final clinical decisions must be made by a licensed physician.")
    
    c.save()
    return file_path
