import streamlit as st
from huggingface_hub import InferenceClient
import re

# Hugging Face setup
hf_token = st.secrets["HF_TOKEN"]
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)

st.title("✍️ Writing Agent")
st.markdown("Generate and edit your paper section by section using JBR style.")

# Section list
sections = [
    "Abstract", "Introduction", "Literature Review",
    "Hypotheses/Framework", "Methodology", "Results",
    "Discussion", "Conclusion"
]

selected_section = st.selectbox("Choose the section to work on:", sections)

# Init session storage for drafts
if "drafts" not in st.session_state:
    st.session_state.drafts = {section: "" for section in sections}

# 🧠 Load structure-based notes from StructureAgent
structure_notes = ""
if "structure_plan" in st.session_state:
    pattern = rf"{selected_section}[\s\S]*?(?=\n[A-Z][a-z]+:|\Z)"
    match = re.search(pattern, st.session_state.structure_plan, re.IGNORECASE)
    if match:
        structure_notes = match.group(0).strip()
        st.markdown("💡 **Plan from StructureAgent:**")
        st.info(structure_notes)

# Editable notes box
notes = st.text_area(
    label="Add your own notes or modify the suggestion below:",
    value=structure_notes,
    height=150
)

# Hugging Face generation
def generate_draft(prompt):
    return client.text_generation(
        prompt=prompt,
        max_new_tokens=500,
        temperature=0.7,
        stop_sequences=["###"]
    )

# Generate button
if st.button("🧠 Generate Draft with AI"):
    with st.spinner("Generating..."):
        full_prompt = f"""You are a research assistant helping write the {selected_section} section of a Journal of Business Research article.

Instructions: Write in a formal, structured academic tone suitable for peer-reviewed publication. Be concise and conceptually sound.

User Notes:
{notes}

Write the section below:
"""
        output = generate_draft(full_prompt).strip()
        st.session_state.drafts[selected_section] = output
        st.success(f"{selected_section} draft updated.")

# Edit the draft
st.text_area(
    label=f"📝 Edit your {selected_section} draft below:",
    value=st.session_state.drafts[selected_section],
    height=300,
    key=f"{selected_section}_edit"
)
