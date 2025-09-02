from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from schemas import Requirement, TestCase

from transformers import pipeline

# Initialize FastAPI
app = FastAPI()

# Load HuggingFace model
generator = pipeline(
    "text-generation",
    model="google/gemma-2b",
    device=-1  # CPU
)

# ---- New request model to match app.py ----
class GenerateRequest(BaseModel):
    requirements: List[Requirement]
    use_ai: bool = True

@app.post("/generate")
def generate(req: GenerateRequest):
    testcases = []

    for i, r in enumerate(req.requirements, start=1):
        if req.use_ai:
            # AI prompt
            prompt = (
                f"Generate a detailed healthcare test case for the requirement:\n"
                f"Requirement: {r.text}\n"
                f"Include: description, 3-5 test steps, expected result, and compliance tags (like HIPAA, GDPR).\n\n"
            )

            output = generator(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)[0]["generated_text"]

            # crude parsing
            lines = [line.strip() for line in output.split("\n") if line.strip()]
            description = lines[0] if lines else f"Test case for: {r.text}"
            steps = [l for l in lines if l.lower().startswith(("step", "1", "2", "3", "-"))]
            expected = next((l for l in lines if "expected" in l.lower()), "System behaves correctly")
            tags = [tag for tag in ["HIPAA", "GDPR", "IEC-62304"] if tag in output]

        else:
            # fallback static logic
            description = f"Validate requirement: {r.text}"
            steps = [
                "1) Prepare test environment with anonymized patient data",
                f"2) Execute requirement: {r.text}",
                "3) Validate outcome against healthcare compliance standards"
            ]
            expected = "System behaves correctly"
            tags = ["IEC-62304", "HIPAA", "GDPR"]

        tc = TestCase(
            id=f"TC-{i:03}",
            requirement_id=r.id,
            description=description,
            steps=steps,
            expected_result=expected,
            compliance_tags=tags
        )
        testcases.append(tc)

    return testcases
