
from utils.model_utils import call_llm

try:
    result = call_llm("Summarize the importance of ethical marketing in business research.")
    print("✅ Response received:\n", result)
except Exception as e:
    print("❌ Error calling LLM:", e)
