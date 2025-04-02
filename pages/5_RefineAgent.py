from utils.model_utils import call_llm
import streamlit as st

st.title("🔍 Refine Agent")
st.markdown("Refine and enhance your drafted research paper sections.")

# Ensure drafts exist in session state
if "drafts" not in st.session_state or not st.session_state.drafts:
    st.warning("Please generate and save drafts using the Writing Agent first.")
    st.stop()

# Display current drafts
st.markdown("### 📝 Current Drafts")
for section, content in st.session_state.drafts.items():
    st.markdown(f"**{section}**")
    st.text_area(f"{section} Section:", value=content, height=150, key=f"{section}_draft", disabled=True)

# Select section to refine
section_to_refine = st.selectbox("Select a section to refine:", list(st.session_state.drafts.keys()))

# Refine the selected section
if st.button(f"🔧 Refine {section_to_refine} Section"):
    with st.spinner(f"Refining the {section_to_refine} section..."):
        prompt = f"""You are an academic research assistant tasked with refining the '{section_to_refine}' section of a research paper.

Current draft of the '{section_to_refine}' section:

{st.session_state.drafts[section_to_refine]}

Please improve the clarity, coherence, and academic rigor of this section. Ensure that the language is formal and that the content aligns with standard academic conventions.

Provide the refined version below:
"""
        try:
            response = call_llm(prompt).strip()
            st.session_state.drafts[section_to_refine] = response
            st.markdown(f"### ✨ Refined {section_to_refine} Section")
            st.text_area(f"{section_to_refine} Section:", value=response, height=400, key=f"{section_to_refine}_refined")
        except Exception as e:
            st.error(f"Error: {e}")

# Save refined drafts to session
if st.session_state.get("drafts"):
    if st.button("✅ Save Refined Drafts"):
        st.success("Refined drafts saved.")
