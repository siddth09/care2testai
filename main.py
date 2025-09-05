import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI

app = FastAPI()

# 🔑 Friendli API client (OpenAI compatible)
client = OpenAI(
    api_key=os.getenv("FRIENDLI_TOKEN"),
    base_url="https://api.friendli.ai/dedicated/v1",  # ✅ generic base for dedicated endpoints
)

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

    for idx, requirement in enumerate(req.requirements, start=1):
        # Generate description using Friendli AI if enabled
        if req.use_ai:
            try:
                chat_completion = client.chat.completions.create(
                    model="deph4wl8wycxqqj",  # ✅ use your endpoint ID here
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an AI that generates structured, concise test cases for healthcare software requirements.",
                        },
                        {
                            "role": "user",
                            "content": f"Requirement: {requirement.text}\nGenerate one concise test case description.",
                        },
                    ],
                    max_tokens=200,
                )
                description = chat_completion.choices[0].message.content.strip()
            except Exception as e:
                description = f"Failed: {str(e)}"
        else:
            description = f"Manual test case for: {requirement.text}"

        # Generate meaningful steps
        steps = [
            f"Verify that: {requirement.text}",
            "Check system behavior according to requirement",
            "Validate expected outcome against healthcare compliance standards",
        ]

        test_cases.append(
            TestCase(
                id=f"TC-{idx}",
                requirement_id=requirement.id,
                description=description,
                steps=steps,
                expected_result="Requirement satisfied",
                compliance_tags=["HIPAA", "GDPR", "IEC 62304", "FDA"],
            )
        )

    return test_cases
