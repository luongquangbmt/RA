import streamlit as st
from utils.model_utils import call_llm
import fitz
import os
import tempfile
from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_index.core import (
    Settings, VectorStoreIndex, SimpleDirectoryReader,
    StorageContext, load_index_from_storage
)
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

st.title("📚 Literature Review Agent (Detailed Summary Mode)")

# === Email Context ===
if "user_email" not in st.session_state or not st.session_state.user_email:
    st.warning("Please return to the homepage and enter your email to start.")
    st.stop()

with st.sidebar:
    st.markdown(f"👤 **Logged in as:** `{st.session_state.user_email}`")
    if st.button("🔁 Log out / Reset"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

# === Per-user RAG storage ===
username = st.session_state.user_email.split("@")[0].replace(".", "_")
DATA_DIR = f"rag_storage/{username}/documents"
INDEX_DIR = f"rag_storage/{username}/index"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

uploaded_files = st.file_uploader("📤 Upload PDF documents", type="pdf", accept_multiple_files=True)

def extract_text_from_pdf(upload):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(upload.read())
        tmp_path = tmp.name
    text = ""
    with fitz.open(tmp_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# === Detailed summary with structured academic prompt ===
if uploaded_files:
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        cleaned_text = text[:8000].replace("\n", " ").replace("\r", " ").strip()

        detailed_prompt = f"""You are an academic research assistant. Carefully read the following excerpt from a research paper.
Write a detailed, structured summary that would help a researcher understand the paper’s contributions without reading the full text.

Your summary must include:
- The main research question and why it matters
- The theoretical background or motivation
- Methodology: type of studies, number of participants, materials used
- Key findings, including moderators and mediators
- Practical implications for branding, marketing, or design
- Contributions to existing academic literature

Use a formal and concise academic tone suitable for a literature review section.
Avoid generalities—focus on what was *actually* found and why it matters.

Paper Text:
{cleaned_text}
"""

        response = call_llm(detailed_prompt)
        st.text_area(f"🧾 Detailed Summary of {file.name}", value=response.strip(), height=400)

        editable_summary = st.text_area(
            f"✏️ Edit Summary for {file.name}",
            value=response.strip(),
            height=400,
            key=f"editable_{file.name}"
        )

        if st.button(f"✅ Save '{file.name}' to Literature Review"):
            if "drafts" not in st.session_state:
                st.session_state.drafts = {}
            st.session_state.drafts[f"Literature Review: {file.name}"] = editable_summary.strip()
            st.success(f"Saved summary of '{file.name}' to your draft.")
