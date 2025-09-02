import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")  # Set in Render Environment

class Requirement(BaseModel):
    id: str
    text: str

class GenerateRequest(BaseModel):
    requirements: List[Requirement]
    use_ai: bool = True

class TestCase(BaseModel):
    id: str
    requirement_id: str
    description: str
    steps: List[str]
    expected_result: str
    compliance_tags: List[str] = []

@app.post("/generate", response_model=List[TestCase])
def generate(req: GenerateRequest):
    test_cases = []
    for idx, requirement in enumerate(req.requirements, start=1):
        if req.use_ai:
            response = requests.post(
                "https://api-inference.huggingface.co/models/google/flan-t5-small",
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                json={"inputs": f"Requirement: {requirement.text}\nGenerate one test case."},
                timeout=30
            )
            if response.status_code == 200:
                try:
                    result = response.json()[0]["generated_text"]
                    description = result.split("\n")[0]
                except Exception:
                    description = "AI response parsing error"
            else:
                description = f"Failed: {response.text}"
        else:
            description = f"Manual test case for: {requirement.text}"

        test_cases.append(
            TestCase(
                id=f"TC-{idx}",
                requirement_id=requirement.id,
                description=description,
                steps=["Step 1", "Step 2", "Step 3"],
                expected_result="Requirement satisfied",
                compliance_tags=["HIPAA", "GDPR", "IEC 62304", "FDA"]
            )
        )
    return test_cases
