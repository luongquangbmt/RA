from utils.model_utils import call_llm
import streamlit as st

st.title("📚 Literature Review Agent")
st.markdown("Generate a literature review based on your research idea.")

# Ensure a research idea exists in session state
if "research_idea" not in st.session_state or not st.session_state.research_idea.get("output"):
    st.warning("Please generate and save a research idea using the Idea Agent first.")
    st.stop()

# Display current research idea
st.markdown("### 📝 Current Research Idea")
st.text_area("Research Idea:", value=st.session_state.research_idea["output"], height=150, disabled=True)

# Generate literature review
if st.button("📖 Generate Literature Review"):
    with st.spinner("Gathering relevant literature..."):
        prompt = f"""You are an academic research assistant tasked with conducting a literature review.

Based on the following research idea:

{st.session_state.research_idea["output"]}

Perform the following tasks:
1. Identify key themes and findings from recent studies related to the research idea.
2. Highlight gaps or controversies in the existing literature.
3. Suggest how these gaps can inform the current research.

Use formal academic language and provide citations where appropriate.
"""
        try:
            response = call_llm(prompt).strip()
            st.session_state.lit_review = response
            st.markdown("### 📄 Generated Literature Review")
            st.text_area("Edit below if needed:", value=response, height=400, key="lit_review_text")
        except Exception as e:
            st.error(f"Error: {e}")

# Save to session
if st.session_state.get("lit_review"):
    if st.button("✅ Save Literature Review"):
        st.success("Literature review saved.")
