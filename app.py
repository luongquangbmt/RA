import streamlit as st
from huggingface_hub import InferenceClient
from docx import Document
from docx.shared import Pt
import tempfile

# Streamlit page config
st.set_page_config(page_title="JBR Writing Assistant", layout="wide")

# Hugging Face API setup
hf_token = st.secrets["HF_TOKEN"]
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)

# Available sections
sections = [
    "Abstract", "Introduction", "Literature Review",
    "Hypotheses/Framework", "Methodology", "Results", "Discussion", "Conclusion"
]

# UI
st.title("📄 JBR Writing Assistant – Now with DOCX Export")
section = st.selectbox("Select the section you want to generate:", sections)
user_input = st.text_area("Describe your research topic, question, or notes:", height=200)

# Hugging Face inference
def generate_with_hf(prompt):
    return client.text_generation(
        prompt=prompt,
        max_new_tokens=500,
        temperature=0.7,
        stop_sequences=["###"]
    )

# DOCX generator
def generate_docx(content, section_title):
    doc = Document()
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Times New Roman"
    font.size = Pt(12)

    doc.add_heading("Journal of Business Research Style Draft", 0)
    doc.add_heading(section_title, level=1)

    for paragraph in content.strip().split("\n\n"):
        doc.add_paragraph(paragraph.strip())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        doc.save(tmp.name)
        return tmp.name

# Generation logic
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
                output = generate_with_hf(full_prompt).strip()
                st.markdown("### ✨ Draft Output:")
                draft = st.text_area("Edit your draft below:", value=output, height=300, key="editable_draft")

                # DOCX Export
                if st.button("📥 Download as Word (.docx)"):
                    docx_path = generate_docx(draft, section)
                    with open(docx_path, "rb") as f:
                        st.download_button(
                            label="Download .docx",
                            data=f,
                            file_name=f"{section.lower().replace(' ', '_')}_draft.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )

                st.success("Draft generated using Mistral on Hugging Face!")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
