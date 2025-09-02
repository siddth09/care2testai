from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from schemas import Requirement, TestCase
import os

# Optional: Google Generative AI (Gemini)
try:
    import google.generativeai as genai
    GEMINI_KEY = os.getenv("GEMINI_API_KEY", None)
    if GEMINI_KEY:
        genai.configure(api_key=GEMINI_KEY)
    else:
        print("⚠️ No GEMINI_API_KEY found, AI mode will fallback to static")
except ImportError:
    genai = None
    GEMINI_KEY = None
    print("⚠️ google-generativeai not installed, AI mode disabled")

app = FastAPI()

class GenerateRequest(BaseModel):
    requirements: List[Requirement]
    use_ai: bool = False

@app.post("/generate")
def generate(req: GenerateRequest):
    testcases = []

    if req.use_ai and genai and GEMINI_KEY:
        # --- AI generation ---
        model = genai.GenerativeModel("gemini-1.5-flash")
        for i, r in enumerate(req.requirements, start=1):
            prompt = f"""
            Convert this healthcare software requirement into a detailed test case:
            Requirement: "{r.text}"
            
            Return JSON with fields:
            - description
            - steps (as list)
            - expected_result
            - compliance_tags (list)
            """
            try:
                resp = model.generate_content(prompt)
                tc_json = resp.text.strip()

                # quick parse to dict (avoid full eval for safety)
                import json
                data = json.loads(tc_json)

                tc = TestCase(
                    id=f"TC-{i:03}",
                    requirement_id=r.id,
                    description=data.get("description", f"Validate: {r.text}"),
                    steps=data.get("steps", [f"Execute requirement: {r.text}"]),
                    expected_result=data.get("expected_result", "System behaves correctly"),
                    compliance_tags=data.get("compliance_tags", ["IEC-62304"])
                )
            except Exception as e:
                print(f"AI failed, falling back. Error: {e}")
                tc = TestCase(
                    id=f"TC-{i:03}",
                    requirement_id=r.id,
                    description=f"Validate requirement: {r.text}",
                    steps=[
                        "1) Prepare test environment",
                        f"2) Execute requirement: {r.text}",
                        "3) Validate against compliance"
                    ],
                    expected_result="System behaves correctly",
                    compliance_tags=["IEC-62304", "HIPAA"]
                )
            testcases.append(tc)
    else:
        # --- Static fallback ---
        for i, r in enumerate(req.requirements, start=1):
            tc = TestCase(
                id=f"TC-{i:03}",
                requirement_id=r.id,
                description=f"Validate requirement: {r.text}",
                steps=[
                    "1) Prepare test environment with anonymized patient data",
                    f"2) Execute requirement: {r.text}",
                    "3) Validate outcome against healthcare compliance standards"
                ],
                expected_result="System behaves correctly",
                compliance_tags=["IEC-62304", "HIPAA", "GDPR"]
            )
            testcases.append(tc)

    return testcases
