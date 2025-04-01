# app.py
import streamlit as st

# Placeholder for your model
def generate_text(prompt):
    # Replace this with your real model logic
    return f"Once upon a time... (continuation of: '{prompt}')"

st.set_page_config(page_title="Creative Writing Assistant", layout="centered")
st.title("📝 Creative Writing Assistant")

prompt = st.text_area("Enter your story prompt:", height=200)

if st.button("Continue Writing"):
    with st.spinner("Generating..."):
        result = generate_text(prompt)
        st.markdown("**Continuation:**")
        st.write(result)
