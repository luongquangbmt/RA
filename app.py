import streamlit as st
from huggingface_hub import InferenceClient

# Hugging Face API setup
hf_token = st.secrets["HF_TOKEN"]
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)

# Streamlit layout
st.set_page_config(page_title="JBR Writing Assistant", layout="wide")
st.title("🤖 JBR Writing Assistant – HuggingFace Edition")

sections = [
    "Abstract", "Introduction", "Literature Review",
    "Hypotheses/Framework", "Methodology", "Results", "Discussion", "Conclusion"
]

section = st.selectbox("Select the section you want to generate:", sections)
user_input = st.text_area("Describe your research topic, question, or notes:", height=200)

def generate_with_hf(prompt):
    return client.text_generation(
        prompt=prompt,
        max_new_tokens=500,
        temperature=0.7,
        stop_sequences=["###"]
    )

if st.button("✍️ Generate Draft"):
    if not user_input.strip():
        st.warning("Please describe your topic.")
    else:
        with st.spinner("Generating with Hugging Face..."):
            full_prompt = f"""### Instruction:
You are a writing assistant specialized in academic business writing. Write the '{section}' section of a Journal of Business Research article in formal academic tone.

### Topic:
{user_input}

### Response:
"""
            try:
                output = generate_with_hf(full_prompt)
                st.markdown("### ✨ Draft Output:")
                st.text_area("Edit your draft below:", value=output.strip(), height=300, key="editable_draft")
                st.success("Draft generated using Mistral on Hugging Face!")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
