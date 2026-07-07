from pydantic import BaseModel, Field
from typing import List

class NLPFeatures(BaseModel):
    entities: List[str] = Field(default_factory=list, description="Extracted medical or symptom entities from the transcript")
    distress_level: str = Field(default="unknown", description="Estimated distress level from speech")
