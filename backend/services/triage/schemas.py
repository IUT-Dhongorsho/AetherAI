from pydantic import BaseModel, Field

class TriageRecommendation(BaseModel):
    triage_level: str = Field(description="The assigned alert level: RED, YELLOW, or GREEN")
    action_text: str = Field(description="The actionable instruction for the pharmacist")
    disease: str = Field(description="The normalized disease name used for the decision")
