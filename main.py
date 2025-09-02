from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from transformers import pipeline

app = FastAPI()

# ✅ Lightweight model for free tier
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    device=-1
)

# -----------------------------
# Request/Response Schemas
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
# API Endpoint
# -----------------------------
@app.post("/generate", response_model=List[TestCase])
def generate(req: GenerateRequest):
    test_cases = []

    for idx, requirement in enumerate(req.requirements, start=1):
        if req.use_ai:
            # Prompt engineering for FLAN-T5
            prompt = (
                f"Requirement: {requirement.text}\n"
                "Generate one software test case with description, steps, and expected result."
            )
            result = generator(prompt, max_length=128, num_return_sequences=1)[0]["generated_text"]

            # Simple parsing fallback
            description = result.split("\n")[0] if result else "Generated test case"
            steps = [f"Step {i+1}" for i in range(3)]
            expected_result = "System behaves as expected"
        else:
            description = f"Manual test case for: {requirement.text}"
            steps = ["Step 1: Review requirement", "Step 2: Execute scenario", "Step 3: Verify outcome"]
            expected_result = "Requirement satisfied"

        test_cases.append(
            TestCase(
                id=f"TC-{idx}",
                requirement_id=requirement.id,
                description=description,
                steps=steps,
                expected_result=expected_result,
                compliance_tags=["HIPAA", "GDPR"]
            )
        )

    return test_cases
