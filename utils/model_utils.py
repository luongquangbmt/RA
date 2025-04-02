import streamlit as st
import requests

# Safely initialize LLM_INDEX
if "LLM_INDEX" not in st.session_state:
    st.session_state["LLM_INDEX"] = 0

# List of LLM providers (free + open access APIs)
LLM_PROVIDERS = [
    {
        "name": "Groq",
        "base_url": "https://api.groq.com/openai/v1",
        "headers": lambda token: {
            "Authorization": f"Bearer {token}"
        },
        "token": st.secrets.get("GROQ_API_KEY", ""),
        "model": "llama-3.2-90b-vision-preview"
    },
    {
        "name": "Groq",
        "base_url": "https://api.groq.com/openai/v1",
        "headers": lambda token: {
            "Authorization": f"Bearer {token}"
        },
        "token": st.secrets.get("GROQ_API_KEY", ""),
        "model": "llama-3.3-70b-versatile"
    },
    {
        "name": "Groq",
        "base_url": "https://api.groq.com/openai/v1",
        "headers": lambda token: {
            "Authorization": f"Bearer {token}"
        },
        "token": st.secrets.get("GROQ_API_KEY", ""),
        "model": "deepseek-r1-distill-llama-70b"
    },
    {
        "name": "OpenRouter",
        "base_url": "https://openrouter.ai/api/v1",
        "headers": lambda token: {
            "Authorization": f"Bearer {token}",
            "HTTP-Referer": "https://yourapp.com",
            "X-Title": "Multi-Agent Research Assistant"
        },
        "token": st.secrets.get("OPENROUTER_API_KEY", ""),
        "model": "huggingfaceh4/zephyr-7b-beta"
    },
    {
        "name": "TogetherAI",
        "base_url": "https://api.together.xyz/v1",
        "headers": lambda token: {
            "Authorization": f"Bearer {token}"
        },
        "token": st.secrets.get("TOGETHER_API_KEY", ""),
        "model": "meta-llama/Llama-2-70b-chat-hf"
    },
    {
        "name": "Fireworks",
        "base_url": "https://api.fireworks.ai/inference/v1",
        "headers": lambda token: {
            "Authorization": f"Bearer {token}"
        },
        "token": st.secrets.get("FIREWORKS_API_KEY", ""),
        "model": "accounts/fireworks/models/llama-v2-13b-chat"
    }
]

def get_active_provider():
    return LLM_PROVIDERS[st.session_state["LLM_INDEX"]]

def switch_to_next_provider():
    st.session_state["LLM_INDEX"] = (st.session_state["LLM_INDEX"] + 1) % len(LLM_PROVIDERS)
    return get_active_provider()

def call_llm(prompt: str):
    for _ in range(len(LLM_PROVIDERS)):
        provider = get_active_provider()
        try:
            url = f"{provider['base_url']}/chat/completions"
            headers = provider["headers"](provider["token"])
            data = {
                "model": provider["model"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }

            response = requests.post(url, json=data, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                raise Exception(f"{provider['name']} error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[⚠️ LLM Fail] {provider['name']}: {e}")
            switch_to_next_provider()

    raise RuntimeError("All LLM providers failed.")