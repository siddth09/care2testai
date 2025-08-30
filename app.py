import streamlit as st
import requests
import json

st.set_page_config(page_title="Care2Test AI Demo", layout="wide")
st.title("💊 Care2Test AI — Requirement → TestCase Prototype")

st.sidebar.header("Backend")
api_base = st.sidebar.text_input(
    "FastAPI URL",
    value="https://care2testai-be.onrender.com"
)

st.markdown(
    """Enter one or more **healthcare requirements** (one per line)."""
)

req_text = st.text_area(
    "Requirements",
    height=200,
    placeholder=(
        "The system shall encrypt patient data.\n"
        "Doctor can update electronic health record.\n"
        "System shall generate alert if BP > 180/120."
    )
)

if st.button("Generate Test Cases"):
    lines = [l.strip() for l in req_text.splitlines() if l.strip()]
    if not lines:
        st.warning("⚠️ Please enter at least one requirement.")
    else:
        payload = [{"id": f"REQ-{i+1}", "text": text} for i, text in enumerate(lines)]
        try:
            resp = requests.post(f"{api_base}/generate", json=payload, timeout=30)
            if resp.status_code == 200:
                tcs = resp.json()
                st.success(f"✅ Generated {len(tcs)} test cases")
                for tc in tcs:
                    with st.expander(f"{tc['id']} — for {tc['requirement_id']}"):
                        st.write("**Description:**", tc["description"])
                        st.write("**Steps:**")
                        for step in tc["steps"]:
                            st.write("-", step)
                        st.write("**Expected Result:**", tc["expected_result"])
                        st.write(
                            "**Compliance Tags:**",
                            ", ".join(tc.get("compliance_tags", []))
                        )
                st.download_button(
                    "📥 Download JSON",
                    data=json.dumps(tcs, indent=2),
                    file_name="testcases.json"
                )
            else:
                st.error(f"Backend error {resp.status_code}: {resp.text}")
        except Exception as e:
            st.error(f"Failed to contact backend: {e}")
