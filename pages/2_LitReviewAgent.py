from utils.model_utils import call_llm
import streamlit as st
import fitz  # PyMuPDF
import tempfile
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
#from llama_index.llms import HuggingFaceLLM
#from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from utils.model_config import HF_MODEL_NAME, HF_TOKEN, switch_to_next_model

def get_inference_client():
    try:
        return get_inference_client()
    except Exception as e:
        switch_to_next_model()
        return get_inference_client()


st.title("📚 LitReview Agent (RAG Enhanced)")
st.markdown("Paste a paper link or upload a PDF — we’ll summarize and synthesize it.")

hf_token = st.secrets["HF_TOKEN"]
#client = get_inference_client()

if "lit_entries" not in st.session_state:
    st.session_state.lit_entries = []

# === 1. Upload or paste link ===
uploaded_file = st.file_uploader("📄 Upload PDF paper", type="pdf")
text = ""

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Extract raw text from PDF
    with fitz.open(tmp_path) as doc:
        for page in doc:
            text += page.get_text()

    st.success("✅ PDF loaded and text extracted.")

    # === 2. RAG setup with LlamaIndex ===
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(f"{tmpdir}/paper.txt", "w") as f:
            f.write(text)

        documents = SimpleDirectoryReader(tmpdir).load_data()

        # Define the LLM + embedding
        service_context = ServiceContext.from_defaults(
            #llm=HuggingFaceLLM(model_name="mistralai/Mistral-7B-Instruct-v0.1", tokenizer_name="mistralai/Mistral-7B-Instruct-v0.1", context_window=2048),
            #embed_model=HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
            llm = HuggingFaceLLM(
                model_name="HuggingFaceH4/zephyr-7b-beta",
                tokenizer_name="HuggingFaceH4/zephyr-7b-beta",
                context_window=2048,
            )
        )

        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        query_engine = index.as_query_engine()

        # === 3. Let user ask question about the paper ===
        user_query = st.text_input("💬 Ask a question about this paper:", value="What are the key findings and contribution?")
        if st.button("🧠 Summarize using paper"):
            with st.spinner("Running RAG..."):
                response = query_engine.query(user_query)
                st.session_state.lit_entries.append({
                    "title": uploaded_file.name,
                    "summary": str(response)
                })
                st.success("Paper summarized and added.")

# === 4. View & synthesize multiple paper summaries ===
if st.session_state.lit_entries:
    st.markdown("### 📝 Your Literature Entries")
    for i, entry in enumerate(st.session_state.lit_entries):
        st.markdown(f"**{i+1}. {entry['title']}**")
        st.markdown(entry["summary"])
        st.markdown("---")

    if st.button("🧩 Synthesize Literature Review"):
        summaries = "\n\n".join(e["summary"] for e in st.session_state.lit_entries)
        prompt = f"""You are writing a literature review based on the following summaries. Write a coherent academic paragraph summarizing key findings, patterns, gaps, and debates.

Summaries:
{summaries}
"""
        result = call_llm(prompt, max_new_tokens=800, temperature=0.7)
        st.text_area("📄 Synthesized Paragraph", value=result.strip(), height=300)
        if st.button("✅ Save to WritingAgent"):
            st.session_state.drafts["Literature Review"] = result.strip()
            st.success("Saved to Literature Review section!")