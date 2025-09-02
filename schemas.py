from pydantic import BaseModel, Field
from typing import List, Optional

class Requirement(BaseModel):
    id: str = Field(..., description="Unique ID of the requirement")
    text: str = Field(..., description="Requirement description in natural language")

class TestCase(BaseModel):
    id: str = Field(..., description="Unique test case ID")
    requirement_id: str = Field(..., description="Reference to Requirement.id")
    description: str = Field(..., description="High-level description of the test case")
    steps: List[str] = Field(default_factory=list, description="List of ordered test steps")
    expected_result: str = Field(..., description="Expected outcome of the test case")
    compliance_tags: Optional[List[str]] = Field(default_factory=list, description="Regulatory/compliance tags (HIPAA, GDPR, etc.)")
