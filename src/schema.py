from pydantic import BaseModel, Field
from typing import List, Optional

class Decision(BaseModel):
    id: str
    title: str
    summary: str
    tags: List[str]
    # הופך את התאריך לאופציונלי
    observed_at: Optional[str] = None 

class Rule(BaseModel):
    id: str
    rule: str
    scope: str 
    notes: Optional[str] = None

class Warning(BaseModel):
    id: str
    area: str
    message: str
    severity: str 

class ProjectKnowledge(BaseModel):
    decisions: List[Decision]
    rules: List[Rule]
    warnings: List[Warning]