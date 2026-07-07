import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import red, green, yellow, black
from datetime import datetime

def generate_pdf_report(patient_id, diagnosis_text, confidence, triage_level, action_text, citations):
    os.makedirs("reports", exist_ok=True)
    file_name = f"aetherai_report_{patient_id}.pdf"
    file_path = os.path.join("reports", file_name)
    
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, height - 1*inch, "AetherAI Clinical Report")
    
    c.setFont("Helvetica", 10)
    c.drawString(1*inch, height - 1.3*inch, f"Report ID: {patient_id}")
    c.drawString(1*inch, height - 1.5*inch, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC")
    
    # Triage Level (Color coded)
    c.setFont("Helvetica-Bold", 14)
    if triage_level == "RED":
        c.setFillColor(red)
        triage_text = "🔴 RED ALERT - URGENT REFERRAL"
    elif triage_level == "YELLOW":
        c.setFillColor(yellow)
        triage_text = "🟡 YELLOW - CLINIC WITHIN 48 HOURS"
    else:
        c.setFillColor(green)
        triage_text = "🟢 GREEN - HOME CARE / OTC"
    
    c.drawString(1*inch, height - 2*inch, triage_text)
    c.setFillColor(black)
    
    # Diagnosis
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, height - 2.5*inch, "Diagnosis:")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 2.8*inch, f"{diagnosis_text} (Confidence: {confidence*100:.1f}%)")
    
    # Action
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, height - 3.3*inch, "Action Required:")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 3.6*inch, action_text)
    
    # Citations
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, height - 4.1*inch, "Citations:")
    y_pos = height - 4.4*inch
    c.setFont("Helvetica", 10)
    for citation in citations:
        c.drawString(1*inch, y_pos, f"• {citation}")
        y_pos -= 0.2*inch
    
    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(1*inch, 0.5*inch, "This is an AI-generated triage recommendation. Final clinical decisions must be made by a licensed physician.")
    
    c.save()
    return file_path
