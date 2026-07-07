from pydantic import BaseModel, Field
from typing import List

class DiagnosisResult(BaseModel):
    primary_diagnosis: str = Field(description="The primary diagnosed respiratory condition (e.g., Pneumonia, Tuberculosis, Normal)")
    confidence: float = Field(description="Confidence score of the diagnosis between 0.0 and 1.0")
    triage_level: str = Field(description="Triage alert level: RED, YELLOW, or GREEN")
    action_text: str = Field(description="Specific, actionable instructions for the pharmacist (e.g., Refer immediately, No antibiotics needed)")
    citations: List[str] = Field(default_factory=list, description="List of clinical guidelines or sources cited for the decision")
