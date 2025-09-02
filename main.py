import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")  # Make sure HF_TOKEN is set in Render Environment
HF_MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-small"  # Public T5 model

# -----------------------------
# Models
# -----------------------------
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

# -----------------------------
# Root endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "API is live!"}

# -----------------------------
# Health endpoint
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Generate test cases
# -----------------------------
@app.post("/generate", response_model=List[TestCase])
def generate(req: GenerateRequest):
    test_cases = []

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    for idx, requirement in enumerate(req.requirements, start=1):
        # Generate description using HF AI if enabled
        if req.use_ai:
            payload = {"inputs": f"Requirement: {requirement.text}\nGenerate one test case."}
            try:
                response = requests.post(HF_MODEL_URL, headers=headers, json=payload, timeout=30)
                response.raise_for_status()  # Raise exception for HTTP errors

                result_json = response.json()
                if isinstance(result_json, list) and "generated_text" in result_json[0]:
                    description = result_json[0]["generated_text"].split("\n")[0]
                else:
                    description = "AI response parsing error"
            except requests.exceptions.RequestException as e:
                description = f"Failed: {str(e)}"
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
