"""
Mock Notification Service for AetherAI.
In production, this would send SMS via Twilio or WhatsApp via Meta API.
"""

def send_alert(phone_number: str, triage_level: str, action_text: str):
    """
    Simulates sending an SMS/WhatsApp alert to the pharmacist or health worker.
    """
    print(f"📱 [MOCK SMS] To: {phone_number}")
    print(f"   Triage: {triage_level}")
    print(f"   Action: {action_text}")
    print("   (In production, this would send a real SMS)")
    
    # Future implementation:
    # if triage_level == "RED":
    #     # Send high-priority SMS via Twilio
    #     pass
    return True
