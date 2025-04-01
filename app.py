import streamlit as st
from huggingface_hub import InferenceClient
from weasyprint import HTML
import tempfile

# Set Streamlit page config
st.set_page_config(page_title="JBR Writing Assistant", layout="wide")

# Hugging Face model setup
hf_token = st.secrets["HF_TOKEN"]
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=hf_token)

# Sections typically found in a Journal of Business Research paper
sections = [
    "Abstract", "Introduction", "Literature Review",
    "Hypotheses/Framework", "Methodology", "Results", "Discussion", "Conclusion"
]

# Streamlit UI
st.title("📄 JBR Writing Assistant – With Hugging Face & PDF Export")
section = st.selectbox("Select the section you want to generate:", sections)
user_input = st.text_area("Describe your research topic, question, or notes:", height=200)

# Hugging Face generation function
def generate_with_hf(prompt):
    return client.text_generation(
        prompt=prompt,
        max_new_tokens=500,
        temperature=0.7,
        stop_sequences=["###"]
    )

# WeasyPrint PDF generator
def generate_pdf_weasy(content, section_title):
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Times New Roman', serif;
                font-size: 12pt;
                line-height: 1.5;
                margin: 1.25in;
            }}
            h1 {{
                text-align: center;
                font-size: 16pt;
                font-weight: bold;
            }}
            h2 {{
                font-size: 14pt;
                font-weight: bold;
                margin-top: 30px;
            }}
            p {{
                text-align: justify;
            }}
        </style>
    </head>
    <body>
        <h1>Journal of Business Research Style Draft</h1>
        <h2>{section_title}</h2>
        <p>{content.replace('\n', '<br><br>')}</p>
    </body>
    </html>
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        HTML(string=html).write_pdf(f.name)
        return f.name

# Generation logic
if st.button("✍️ Generate Draft"):
    if not user_input.strip():
        st.warning("Please describe your topic.")
    else:
        with st.spinner("Generating with Hugging Face..."):
            full_prompt = f"""### Instruction:
You are a writing assistant specialized in academic business writing. Write the '{section}' section of a Journal of Business Research article in formal academic tone.

### Topic:
{user_input}

### Response:
"""
            try:
                output = generate_with_hf(full_prompt).strip()
                st.markdown("### ✨ Draft Output:")
                draft = st.text_area("Edit your draft below:", value=output, height=300, key="editable_draft")

                # PDF export logic
                if st.button("📥 Download as PDF"):
                    pdf_path = generate_pdf_weasy(draft, section)
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download PDF",
                            data=f,
                            file_name=f"{section.lower().replace(' ', '_')}_draft.pdf",
                            mime="application/pdf"
                        )

                st.success("Draft generated using Mistral on Hugging Face!")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
