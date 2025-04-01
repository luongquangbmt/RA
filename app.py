import streamlit as st
from openai import OpenAI

# Set page layout
st.set_page_config(page_title="JBR Writing Assistant", layout="wide")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define JBR article sections
sections = [
    "Abstract",
    "Introduction",
    "Literature Review",
    "Hypotheses/Framework",
    "Methodology",
    "Results",
    "Discussion",
    "Conclusion"
]

st.title("🧠 JBR Writing Assistant – WritingAgent")

# Choose section
section = st.selectbox("Which section would you like to write?", sections)

# User input area
user_input = st.text_area("Describe your research topic, focus, or notes for this section:", height=200)

# Generate output
if st.button("✍️ Generate Draft"):
    if user_input.strip() == "":
        st.warning("Please enter a research topic or idea.")
    else:
        with st.spinner("Generating content..."):
            # Compose the full prompt
            prompt = f"""
You are a writing assistant helping with an academic article in the Journal of Business Research (JBR) style.

Write the **{section}** section of a research paper based on the following idea or notes:
\"\"\"{user_input}\"\"\"

Use a formal academic tone, concise structure, and JBR formatting conventions.
"""
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a writing assistant specialized in academic business research."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )

                output = response.choices[0].message.content.strip()
                st.markdown("### ✨ Generated Draft:")
                st.text_area("You can now edit this draft below:", value=output, height=300, key="editable_draft")

                st.success("Draft generated. Feel free to revise or copy it!")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
