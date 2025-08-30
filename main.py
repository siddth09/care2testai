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
                "1) Prepare environment",
                f"2) Execute requirement: {req.text}",
                "3) Validate outcome"
            ],
            expected_result="System behaves correctly",
            compliance_tags=["Demo"]
        )
        testcases.append(tc)
    return testcases

