from fastapi import FastAPI
from typing import List
from schemas import Requirement, TestCase

from transformers import pipeline

# Initialize FastAPI
app = FastAPI()

# Load HuggingFace model (Gemma-2B or any small model available)
# Using a text-generation pipeline
generator = pipeline(
    "text-generation",
    model="google/gemma-2b",
    device=-1  # -1 = CPU, 0 = GPU
)

@app.post("/generate")
def generate(requirements: List[Requirement]):
    testcases = []

    for i, req in enumerate(requirements, start=1):
        # Create a prompt for the AI
        prompt = (
            f"Generate a detailed healthcare test case for the requirement:\n"
            f"Requirement: {req.text}\n"
            f"Include: description, 3-5 test steps, expected result, and compliance tags (like HIPAA, GDPR).\n\n"
        )

        # Generate response
        output = generator(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)[0]["generated_text"]

        # --- simple parsing (fallback if AI response is messy) ---
        # We'll extract chunks by splitting lines
        lines = [line.strip() for line in output.split("\n") if line.strip()]
        description = lines[0] if lines else f"Test case for: {req.text}"
        steps = [l for l in lines if l.lower().startswith(("-", "step", "1", "2", "3"))]
        expected = next((l for l in lines if "expected" in l.lower()), "System behaves correctly")
        tags = [tag for tag in ["HIPAA", "GDPR", "IEC-62304"] if tag in output]

        tc = TestCase(
            id=f"TC-{i:03}",
            requirement_id=req.id,
            description=description,
            steps=steps or [
                f"Execute: {req.text}",
                "Check compliance with healthcare standards"
            ],
            expected_result=expected,
            compliance_tags=tags or ["General-Healthcare"]
        )
        testcases.append(tc)

    return testcases
