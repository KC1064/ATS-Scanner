# Load environment variables 
from dotenv import load_dotenv
load_dotenv()

# Import packages
import streamlit as st
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to extract text from uploaded PDF
def extract_text_from_pdf(pdf_file):
    if pdf_file is not None:
        try:
            pdf = PdfReader(pdf_file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n\n"
            return text
        except Exception as e:
            st.error(f"❌ Error extracting text from PDF: {str(e)}")
            return None
    else:
        raise FileNotFoundError("No File Found")

# Gemini response function
def gemini_response(text_content, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    full_prompt = f"""
    RESUME CONTENT:
    {text_content}
    
    INSTRUCTIONS:
    {prompt}
    """
    response = model.generate_content(full_prompt)
    return response.text


st.set_page_config(page_title="📄 ATS Resume Scanner", page_icon="🤖", layout="centered")


st.markdown("<h1 style='text-align: center;'>📄 ATS Resume Scanner 🤖</h1>", unsafe_allow_html=True)
st.markdown("### 🔍 Scan your resume against job descriptions and level up your application!")


input_role = st.text_input("🎯 Job Role", placeholder="e.g., Frontend Developer", key="role")
input_text = st.text_area("📝 Job Description", placeholder="Paste the job description here...", key="input")

uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")

st.markdown("### ✨ Choose what you want to do:")
btn_style = """
<style>
    div.stButton > button {
        width: 100%;
        height: 3em;
        font-size: 1.1em;
    }
</style>
"""
st.markdown(btn_style, unsafe_allow_html=True)

btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1], gap="medium")

with btn_col1:
    submit_btn1 = st.button("🔍 Overview")
with btn_col2:
    submit_btn2 = st.button("🛠️ Tips to Upgrade")
with btn_col3:
    submit_btn3 = st.button("📊 ATS Score")

# --- SYSTEM PROMPTS ---
sys_prompt1 = f"""
Acts as Human Resource manager who has an experience of 20+ years. He is very experienced in the {input_role} field and is vastly knowledgeable.

Working:
1. You need to analyze the given resume against the job descriptions: {input_text} and create a list of what the user has done right and what the user has done wrong.
2. Also tell the user an overall summary of his resume.
"""

sys_prompt2 = f"""
You are expert content writer and very experienced HR who has experience in crafting very well versed resumes that will pass through ATS scanners very easily. Resumes crafted by you have an ATS score of at least 85+.

You are assigned a job to give insights to a user who is applying for a job role of {input_role} and the job description are as follows {input_text}.

You need to tell the user what parts need modification and what they are.
"""

sys_prompt3 = f"""
You are a very advanced ATS software who is very adept in scanning resume against the given role {input_role} and job description: {input_text}.

You need to follow this sequence and generate the response accordingly:
1. Understand the job role and job description
2. Find the key words and highlight and match them to the user's resume
3. Then calculate an ATS score based on your calculations
4. At last give only the ATS score nothing else
"""


if submit_btn1:
    if uploaded_file is not None and input_role.strip():
        with st.spinner("🔄 Analyzing resume..."):
            text_content = extract_text_from_pdf(uploaded_file)
            if text_content:
                response = gemini_response(text_content, sys_prompt1)
                st.markdown("### 📋 Overview Result")
                st.write(response)
            else:
                st.error("Could not extract text. Try another file.")
    else:
        st.warning("⚠️ Please upload your resume and enter the job role.")

if submit_btn2:
    if uploaded_file is not None and input_role.strip() and input_text.strip():
        with st.spinner("🔄 Generating upgrade tips..."):
            text_content = extract_text_from_pdf(uploaded_file)
            if text_content:
                response = gemini_response(text_content, sys_prompt2)
                st.markdown("### 🛠️ Tips to Upgrade")
                st.write(response)
            else:
                st.error("Could not extract text. Try another file.")
    else:
        st.warning("⚠️ Please fill in all the details (Job Role, Job Description, Resume).")

if submit_btn3:
    if uploaded_file is not None and input_role.strip() and input_text.strip():
        with st.spinner("🔍 Scanning for ATS Score..."):
            text_content = extract_text_from_pdf(uploaded_file)
            if text_content:
                response = gemini_response(text_content, sys_prompt3)
                st.markdown("### 📊 ATS Score")
                st.write(response)
            else:
                st.error("Could not extract text. Try another file.")
    else:
        st.warning("⚠️ Please fill in all the details (Job Role, Job Description, Resume).")


st.markdown("""
<br><hr>
<div style='text-align: center; font-size: 16px'>
    🧠 Made with <span style='color:red;'>❤️</span> for developers who love applying smart 😎
</div>
""", unsafe_allow_html=True)
