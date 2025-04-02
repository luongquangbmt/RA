from utils.model_utils import call_llm
import streamlit as st

st.title("✍️ Writing Agent")
st.markdown("Draft sections of your research paper based on the structured outline.")

# Ensure a structure plan exists in session state
if "structure_plan" not in st.session_state or not st.session_state.structure_plan:
    st.warning("Please generate and save a structure plan using the Structure Agent first.")
    st.stop()

# Display current structure plan
st.markdown("### 🏗️ Current Structure Plan")
st.text_area("Structure Plan:", value=st.session_state.structure_plan, height=150, disabled=True)

# Initialize drafts in session state if not present
if "drafts" not in st.session_state:
    st.session_state.drafts = {}

# Generate drafts for each section
sections = ["Introduction", "Literature Review", "Methodology", "Results", "Discussion", "Conclusion"]

for section in sections:
    if st.button(f"📝 Draft {section}"):
        with st.spinner(f"Writing the {section} section..."):
            prompt = f"""You are an academic research assistant tasked with drafting the '{section}' section of a research paper.

Based on the following structure plan:

{st.session_state.structure_plan}

Draft the '{section}' section with appropriate content and depth.

Use formal academic language.
"""
            try:
                response = call_llm(prompt).strip()
                st.session_state.drafts[section] = response
                st.markdown(f"### ✍️ Drafted {section} Section")
                st.text_area(f"{section} Section:", value=response, height=400, key=f"{section}_text")
            except Exception as e:
                st.error(f"Error: {e}")

# Save drafts to session
if st.session_state.get("drafts"):
    if st.button("✅ Save Drafts"):
        st.success("Drafts saved.")
