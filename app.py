import streamlit as st
from huggingface_hub import InferenceClient
from docx import Document
from docx.shared import Pt
from io import BytesIO

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
st.title("📄 JBR Writing Assistant – Hugging Face + DOCX Export")
section = st.selectbox("Select the section you want to generate:", sections)
user_input = st.text_area("Describe your research topic, question, or notes:", height=200)

# Hugging Face generation
def generate_with_hf(prompt):
    return client.text_generation(
        prompt=prompt,
        max_new_tokens=500,
        temperature=0.7,
        stop_sequences=["###"]
    )

# DOCX export in-memory (Streamlit Cloud compatible)
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

    buffer = BytesIO()
    doc.save(buffer
