import streamlit as st
from huggingface_hub import InferenceClient
from utils.model_config import HF_MODEL_NAME, HF_TOKEN, switch_to_next_model

def get_inference_client():
    from huggingface_hub import InferenceClient
    try:
        return get_inference_client()
    except Exception as e:
        switch_to_next_model()
        return get_inference_client()

# Hugging Face setup
hf_token = st.secrets["HF_TOKEN"]
client = get_inference_client()

st.title("🏗️ Structure Agent")
st.markdown("Design your paper’s structure based on your research idea.")

# Show saved research idea
if "research_idea" in st.session_state:
    st.markdown("#### 🎯 Current Research Topic")
    st.info(st.session_state.research_idea.get("topic", ""))
else:
    st.warning("You haven't defined a research idea yet. Use the IdeaAgent first.")
    st.stop()

# Outline section goals
st.markdown("### 📄 Standard JBR Structure")
section_goals = {
    "Abstract": "Summarize the research problem, method, findings, and contribution.",
    "Introduction": "Introduce the research context, problem, importance, and overview.",
    "Literature Review": "Situate the research in past work, define key terms and gaps.",
    "Hypotheses/Framework": "Present theory, conceptual model, and hypotheses.",
    "Methodology": "Describe sample, variables, research design, and data collection.",
    "Results": "Report findings, analysis, tests of hypotheses.",
    "Discussion": "Interpret results, implications, limitations, future work.",
    "Conclusion": "Wrap up, restate contributions, and suggest broader impacts."
}

# User triggers AI-generated outline
if st.button("📐 Generate Section-by-Section Plan"):
    with st.spinner("Designing structure..."):
        topic = st.session_state.research_idea["topic"]
        summary = st.session_state.research_idea["output"]
        prompt = f"""You are an assistant helping outline a Journal of Business Research article.

Research Topic: {topic}

Research Summary:
{summary}

For each section below, write a short paragraph (2–4 sentences) describing what the author should write based on the topic.

Sections:
- Abstract
- Introduction
- Literature Review
- Hypotheses/Framework
- Methodology
- Results
- Discussion
- Conclusion

Use formal, clear language for academic planning.
"""
        try:
            response = client.text_generation(prompt, max_new_tokens=800, temperature=0.6)
            st.session_state.structure_plan = response.strip()
            st.markdown("### ✨ Generated Section Plan")
            st.text_area("You can revise the outline here:", value=st.session_state.structure_plan, height=400)
        except Exception as e:
            st.error(f"Error: {e}")

# Export structure to session
if st.session_state.get("structure_plan"):
    if st.button("✅ Save Plan to Session"):
        st.success("Structure plan saved for other agents.")