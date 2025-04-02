import streamlit as st
from huggingface_hub import InferenceClient

# Setup
hf_token = st.secrets["HF_TOKEN"]
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)

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
            response = client.text_generation(prompt, max_new_tokens=600, temperature=0.7).strip()
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
