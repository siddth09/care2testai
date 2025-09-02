from fastapi import FastAPI
from typing import List
from schemas import Requirement, TestCase

app = FastAPI()

@app.post("/generate")
def generate(requirements: List[Requirement]):
    testcases = []
    for i, req in enumerate(requirements, start=1):
        tc = TestCase(
            id=f"TC-{i:03}",
            requirement_id=req.id,
            description=f"Validate requirement: {req.text}",
            steps=[
                "1) Prepare test environment with anonymized patient data",
                f"2) Execute requirement: {req.text}",
                "3) Validate outcome against healthcare compliance standards"
            ],
            expected_result="System behaves correctly",
            compliance_tags=["IEC-62304", "HIPAA", "GDPR"]
        )
        testcases.append(tc)
    return testcases

