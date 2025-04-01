import streamlit as st
import openai

# Set your OpenAI API key safely via Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if you're on the free tier
        messages=[
            {"role": "system", "content": "You are a creative writing assistant. Help the user write beautiful, imaginative prose."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.9
    )
    return response.choices[0].message.content.strip()

st.set_page_config(page_title="Creative Writing Assistant", layout="centered")
st.title("📝 Creative Writing Assistant")

prompt = st.text_area("Enter your story prompt:", height=200)

if st.button("Continue Writing"):
    with st.spinner("Generating..."):
        result = generate_text(prompt)
        st.markdown("**Continuation:**")
        st.write(result)
