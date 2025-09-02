import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")  # Make sure HF_TOKEN is set in Render Environment

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
        # Generate description using HF AI if enabled
        if req.use_ai:
            hf_url = "https://api-inference.huggingface.co/pipeline/text2text-generation/google/flan-t5-small"
            response = requests.post(
                hf_url,
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

        # Generate simple meaningful steps
        steps = [
            f"Verify that: {requirement.text}",
            "Check system behavior according to requirement",
            "Validate expected outcome against healthcare compliance standards"
        ]

        test_cases.append(
            TestCase(
                id=f"TC-{idx}",
                requirement_id=requirement.id,
                description=description,
                steps=steps,
                expected_result="Requirement satisfied",
                compliance_tags=["HIPAA", "GDPR", "IEC 62304", "FDA"]
            )
        )

    return test_cases
