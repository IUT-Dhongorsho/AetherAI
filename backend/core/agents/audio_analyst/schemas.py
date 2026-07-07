from pydantic import BaseModel, Field
from typing import Dict

class AudioFeatures(BaseModel):
    sample_rate: int = Field(default=16000, description="Sample rate of the processed audio")
    status: str = Field(description="Processing status (Success or Error message)")

class AudioPrediction(BaseModel):
    probabilities: Dict[str, float] = Field(
        description="Dictionary mapping disease classes to their predicted probabilities"
    )
