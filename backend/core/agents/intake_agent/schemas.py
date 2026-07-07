from pydantic import BaseModel, Field
from typing import Optional

class PatientHistory(BaseModel):
    age: Optional[int] = Field(None, description="Age of the patient")
    gender: Optional[str] = Field(None, description="Gender of the patient")
    region: Optional[str] = Field(None, description="Geographical region of the patient")
    fever: Optional[bool] = Field(False, description="Whether the patient has a fever")
    weight_loss: Optional[bool] = Field(False, description="Whether the patient experienced weight loss")
    notes: Optional[str] = Field("", description="Raw notes from the pharmacist")
