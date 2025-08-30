from pydantic import BaseModel
from typing import List, Optional

class Requirement(BaseModel):
    id: str
    text: str

class TestCase(BaseModel):
    id: str
    requirement_id: str
    description: str
    steps: List[str]
    expected_result: str
    compliance_tags: Optional[List[str]] = []

