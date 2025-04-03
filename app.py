import streamlit as st

# === Welcome and Email Prompt ===
st.markdown("""
## 👋 Welcome to the Research Assistant for Journal of Business Research

This assistant helps you generate high-quality research papers with:
- 🧠 AI-assisted idea generation  
- 📚 Literature review from your own PDFs  
- ✍️ Structured writing tools  
- 💾 Personalized draft and citation storage

Enter your email to get started. Your workspace will be saved automatically so you can return to it anytime!
""")

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

st.session_state.user_email = st.text_input(
    "📬 Email",
    value=st.session_state.user_email,
    placeholder="your@email.com"
)

if st.session_state.user_email:
    st.success(f"👋 Welcome back, **{st.session_state.user_email}**! Your workspace is ready.")

if not st.session_state.user_email:
    st.warning("Please enter your email to continue.")
    st.stop()

# You can continue your app logic below this line...
st.markdown("### ✨ Select a page from the sidebar to begin.")
