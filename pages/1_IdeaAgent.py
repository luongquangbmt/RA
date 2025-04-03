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
st.title("🧠 Idea Agent")
st.markdown("Brainstorm your research question, theoretical framework, and contribution idea.")

# User input
topic = st.text_input("Enter your general research topic or area:")
if not topic:
    st.stop()

if "research_idea" not in st.session_state:
    st.session_state.research_idea = {}

# Generate ideas
if st.button("💡 Brainstorm Ideas"):
    with st.spinner("Thinking..."):
        prompt = f"""You are an academic research assistant helping define a research project for a Journal of Business Research paper.

Based on the topic: "{topic}", generate the following:
- 2–3 possible research questions
- Suggested theoretical frameworks or perspectives
- Possible hypotheses or relationships
- Key concepts or variables involved
- Potential academic or practical contributions

Use clear, formal language.
"""
        try:
            response = call_llm(prompt).strip()
            st.session_state.research_idea["topic"] = topic
            st.session_state.research_idea["output"] = response
            st.markdown("### 🧩 Generated Research Directions:")
            st.text_area("Edit below if needed:", value=response, height=400, key="idea_text")
        except Exception as e:
            st.error(f"Error: {e}")

# Save to session
if st.session_state.get("research_idea"):
    if st.button("✅ Save Research Idea"):
        st.success("Research idea saved.")
