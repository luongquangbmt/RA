from utils.model_utils import call_llm
import streamlit as st


# === Display user email and logout/reset ===
if "user_email" not in st.session_state or not st.session_state.user_email:
    st.warning("Please return to the homepage and enter your email to start.")
    st.stop()

with st.sidebar:
    st.markdown(f"👤 **Logged in as:** `{st.session_state.user_email}`")
    if st.button("🔁 Log out / Reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
st.title("🏗️ Structure Agent")
st.markdown("Develop a structured outline for your research paper.")

# Ensure a research idea exists in session state
if "research_idea" not in st.session_state or not st.session_state.research_idea.get("output"):
    st.warning("Please generate and save a research idea using the Idea Agent first.")
    st.stop()

# Display current research idea
st.markdown("### 📝 Current Research Idea")
st.text_area("Research Idea:", value=st.session_state.research_idea["output"], height=150, disabled=True)

# Generate structure
if st.button("📑 Generate Structure"):
    with st.spinner("Organizing the paper structure..."):
        prompt = f"""You are an academic research assistant tasked with structuring a research paper.

Based on the following research idea:

{st.session_state.research_idea["output"]}

Develop a detailed outline for the paper, including:
1. Introduction
2. Literature Review
3. Methodology
4. Results
5. Discussion
6. Conclusion

For each section, provide key points or subheadings that should be addressed.

Use clear, formal language.
"""
        try:
            response = call_llm(prompt).strip()
            st.session_state.structure_plan = response
            st.markdown("### 🏗️ Generated Paper Structure")
            st.text_area("Edit below if needed:", value=response, height=400, key="structure_text")
        except Exception as e:
            st.error(f"Error: {e}")

# Save to session
if st.session_state.get("structure_plan"):
    if st.button("✅ Save Structure Plan"):
        st.success("Structure plan saved.")
