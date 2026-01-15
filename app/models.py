from pydantic import BaseModel, Field
from typing import List

class Threat(BaseModel):
    name: str
    location: str
    danger_rate: int = Field(..., ge=1, le=10) 

class TopThreatsResponse(BaseModel):
    inserted: List[Threat]