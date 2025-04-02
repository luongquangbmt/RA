
from huggingface_hub import InferenceClient
from utils.model_config import HF_MODEL_NAME, HF_TOKEN, switch_to_next_model

def get_inference_client():
    try:
        return InferenceClient(model=HF_MODEL_NAME, token=HF_TOKEN)
    except Exception as e:
        print(f"[Warning] Error loading model {HF_MODEL_NAME}: {e}")
        switch_to_next_model()
        return InferenceClient(model=HF_MODEL_NAME, token=HF_TOKEN)
