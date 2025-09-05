import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# -----------------------------
# Config
# -----------------------------
FRIENDLI_TOKEN = os.getenv("FRIENDLI_TOKEN")  # Set this in Render Environment
FRIENDLI_URL = "https://api.friendli.ai/dedicated/deph4wl8wycxqqj"  # Your endpoint ID is embedded

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

    headers = {
        "Authorization": f"Bearer {FRIENDLI_TOKEN}",
        "Content-Type": "application/json"
    }

    for idx, requirement in enumerate(req.requirements, start=1):
        # Generate description using Friendli AI if enabled
        if req.use_ai:
            payload = {
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an AI that generates test cases for software requirements."
                    },
                    {
                        "role": "user",
                        "content": f"Requirement: {requirement.text}\nGenerate one test case."
                    }
                ],
                "max_tokens": 200
            }

            try:
                response = requests.post(FRIENDLI_URL, headers=headers, json=payload, timeout=30)
                response.raise_for_status()
                result_json = response.json()

                # Friendli’s API is OpenAI-compatible → response structure similar to OpenAI
                if "choices" in result_json and len(result_json["choices"]) > 0:
                    description = result_json["choices"][0]["message"]["content"].strip()
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
