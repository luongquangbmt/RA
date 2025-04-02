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

# Hugging Face API setup
hf_token = st.secrets["HF_TOKEN"]
client = get_inference_client()

st.title("🪞 Refine Agent")
st.markdown("Polish your writing for clarity, tone, and academic style.")

# Ensure content exists
if "drafts" not in st.session_state:
    st.warning("No draft found. Please create content using the Writing Agent first.")
    st.stop()

# Section selector
sections = list(st.session_state.drafts.keys())
selected_section = st.selectbox("Choose a section to refine:", sections)
original_text = st.session_state.drafts[selected_section].strip()

if not original_text:
    st.warning("This section is currently empty. Please write or generate it first.")
    st.stop()

# Refinement options
mode = st.selectbox("Choose refinement style:", [
    "Polish academically",
    "Simplify for clarity",
    "Expand ideas",
    "Make more formal"
])

# Prompt builder
def build_prompt(mode, text):
    instruction = {
        "Polish academically": "Improve this section's academic tone and clarity without changing meaning.",
        "Simplify for clarity": "Make this more concise and easier to understand while preserving detail.",
        "Expand ideas": "Expand on the key ideas to give more depth and completeness.",
        "Make more formal": "Rewrite this in a more formal and professional academic style."
    }[mode]
    
    return f"""### Instruction:
{instruction}

### Section:
{text}

### Response:
"""

# Run refinement
if st.button("🔁 Refine Section"):
    with st.spinner("Refining..."):
        try:
            prompt = build_prompt(mode, original_text)
            result = client.text_generation(prompt, max_new_tokens=600, temperature=0.5)
            refined_text = result.strip()
            st.text_area("🔍 Refined version:", value=refined_text, height=300, key="refined_output")

            # Option to accept changes
            if st.button("✅ Replace original with refined version"):
                st.session_state.drafts[selected_section] = refined_text
                st.success(f"{selected_section} updated with refined version.")
        except Exception as e:
            st.error(f"Error: {e}")