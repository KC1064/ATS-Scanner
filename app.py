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
    

good_resume_details = """
RESUME LANGUAGE SHOULD BE:
- Using action words
- Specific rather than general
- Active rather than passive
- Written to express not impress
- Articulate rather than "flowery"
- Fact-based (quantify and qualify)
- Written for people who scan quickly

TOP SIX RESUME MISTAKES:
- Spelling and grammar errors
- Missing email and phone information
- Using passive language instead of "action" words
- Not well organized, concise, or easy to skim
- Not demonstrating results
- Too long
- Repeated use of same words

DON'T:
- Use personal pronouns (such as I)
- Abbreviate
- Use a narrative style
- Use slang or colloquialisms
- Include a picture
- Include age or gender
- List references
- Start each line with a date

DO:
- Be consistent in format and content
- Make it easy to read and follow, balancing white space
- Use consistent spacing, underlining, italics, bold, and capitalization for emphasis
- List headings (such as Experience) in order of importance
- Within headings, list information in reverse chronological order (most recent first)
- Avoid information gaps such as a missing summer

Then go through the each section that are present in the resume and analyze according to 
this points:

PROFILE Section
- A brief statement that highlights your career goals. Ideal for candidates with 
limited professional experience, such as recent college or high school graduates.
- A concise overview using active language to showcase your relevant experience, skills, 
and accomplishments. Best for candidates with some professional background.

EDUCATION Section
- Check for proper formatting.
- Add the degree and education.

EXPERIENCE Section
- Ideally each experience should have 2-3 points.
- Make sure the dates are accurate and consistent in style, include the
year and month
- Scan the whole section for repetetive actions words and replace with different
action words.

SKILLS Section
- Add tech stack under different subheadings
- Example: Web Development: HTML, CSS, React, NextJS, Express

PROJECTS Section
- Ideally 3-4 projects with 2-3 points each.
- Mention the skills you learned or used.
- Scan the whole section for repetetive actions words and replace with different
action words.

ACHIEVEMENTS & ROLES Section
- Write proper action words to say your achievements and roles 
- Scan the whole section for repetetive actions words and replace with different
action words.

FOR WHOLE RESUME:
- Don't use repetitive action words.
- Check for spelling and grammar mistakes
"""


# --- SYSTEM PROMPTS ---
sys_prompt1 = f"""
Acts as Human Resource manager who has an experience of 20+ years. You are very experienced in the {input_role} field and are vastly knowledgeable.

Working:
1. Analyze the given resume against the job description: {input_text}
2. Create a concise, point-wise list of what the user has done right and what needs improvement
3. Provide a brief overall summary of the resume in 3-5 bullet points maximum

FORMAT YOUR RESPONSE:
- Use bullet points
- Be direct and specific
- Prioritize the most important points
- Keep the response concise and easy to scan

RESUME BEST PRACTICES:
{good_resume_details}
"""

sys_prompt2 = f"""
You are an expert content writer and very experienced HR who has experience crafting resumes that pass through ATS scanners easily with scores of 85+.

Your task:
1. Analyze the resume for a person applying for: {input_role}
2. Compare it against this job description: {input_text}
3. Provide specific, actionable improvements in a concise, point-wise format

FORMAT YOUR RESPONSE:
- Group feedback by resume sections (Profile, Experience, Skills, etc.)
- Use bullet points for each suggestion
- Be direct and specific
- Include 1-2 examples of how to improve key points
- Suggest the modifications for me to copy.

RESUME BEST PRACTICES:
{good_resume_details}
"""

sys_prompt3 = f"""
You are an advanced ATS software scanning a resume against the role of {input_role} and this job description: {input_text}.

Your task:
1. Identify key skills, qualifications, and requirements from the job description
2. Match the user's resume with these instructions
{good_resume_details}
3. Score each section out of 100 based on relevance.
4. Provide an overall ATS compatibility score by taking average of all the sections score.
5. Suggest specific improvements to increase the match score.

FORMAT YOUR RESPONSE:
- Start with the numerical ATS score prominently displayed
- Provide 3-5 bullet points explaining how the score was calculated
- List top 10 matching keywords found
- List top 10 missing keywords or qualifications
- Keep the entire response concise and scannable
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