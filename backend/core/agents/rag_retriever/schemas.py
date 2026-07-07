from pydantic import BaseModel, Field
from typing import List

class RetrievedDocument(BaseModel):
    title: str = Field(description="Source title of the clinical guideline")
    snippet: str = Field(description="Relevant text snippet retrieved from the document")

class RAGResult(BaseModel):
    documents: List[RetrievedDocument] = Field(default_factory=list, description="List of retrieved guidelines")
