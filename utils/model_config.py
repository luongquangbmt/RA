
import streamlit as st

# List of free and open-access models (ranked by performance)
AVAILABLE_MODELS = [
    "HuggingFaceH4/zephyr-7b-beta",
    "tiiuae/falcon-7b-instruct",
    "mistralai/Mistral-7B-Instruct-v0.1",
    "mosaicml/mpt-7b-instruct",
    "bigscience/bloomz-7b1",
    "meta-llama/Llama-2-7b-chat-hf"
]

# Retrieve Hugging Face token securely
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# Current model index stored in session or fallback to 0
if "HF_MODEL_INDEX" not in st.session_state:
    st.session_state.HF_MODEL_INDEX = 0

# Active model name (first available by default)
HF_MODEL_NAME = AVAILABLE_MODELS[st.session_state.HF_MODEL_INDEX]

def switch_to_next_model():
    """Switch to the next available model."""
    st.session_state.HF_MODEL_INDEX = (st.session_state.HF_MODEL_INDEX + 1) % len(AVAILABLE_MODELS)
    return AVAILABLE_MODELS[st.session_state.HF_MODEL_INDEX]
