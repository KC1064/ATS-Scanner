# # load env variables 
# from dotenv import load_dotenv
# load_dotenv()

# # import packages
# import streamlit as st
# import os
# import io
# import base64
# from PIL import Image
# import pdf2image
# import google.generativeai as genai

# # Configure API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def gemini_response(pdf_content, prompt):
#     model = genai.GenerativeModel('gemini-pro-vision')
#     response = model.generate_content([pdf_content[0], prompt])
#     return response.text

# def pdf_upload(pdf_file):
#     if pdf_file is not None:
#         try:
#             # Convert PDF to images
#             images = pdf2image.convert_from_bytes(pdf_file.read())
            
#             # Reset file pointer
#             pdf_file.seek(0)
            
#             if images:
#                 page = images[0]
#                 img_byte_arr = io.BytesIO()
#                 page.save(img_byte_arr, format='JPEG')
#                 img_byte_arr = img_byte_arr.getvalue()

#                 pdf_parts = [
#                     {
#                         "mime_type": "image/jpeg",
#                         "data": base64.b64encode(img_byte_arr).decode()
#                     }
#                 ]
#                 return pdf_parts
#             else:
#                 st.error("Could not convert PDF to image")
#                 return None
#         except Exception as e:
#             st.error(f"Error processing PDF: {str(e)}")
#             return None
#     else:
#         raise FileNotFoundError('No File Found')

# # Configuration of Streamlit App
# st.set_page_config(page_title="ATS Resume Scanner")
# st.header('ATS Tracking System')
# input_text = st.text_area("Job Description", key="input")
# # Input Roles
# input_role = st.text_area("Enter the Role You are applying for...", key="role")
# uploaded_file = st.file_uploader("Upload Your Resume(PDF)...", type=["pdf"])

# if uploaded_file is not None:
#     st.write('PDF Uploaded Successfully')

# submit_btn1 = st.button("Tell me about Resume")
# submit_btn2 = st.button("How can I improvise my Skills")
# submit_btn3 = st.button("Percentage Match")

# sys_prompt1 = f"""
# Acts as Human Resource manager who has an experience of 20+ years. He is very experienced in the {input_role} field and is vastly knowledgeable.

# Working:
# 1. You need to analyse the given resume against the job descriptions: {input_text} and create a list of what the user has done right and what the user has done wrong.
# 2. Also tell the user an overall summary of his resume.
# """

# sys_prompt2 = f"""
# You are expert content writer and very experienced HR who has experience in crafting very well versed resumes that will pass through ATS scanners very easily. Resumes crafted by you have an ATS score of at least 85+.

# You are assigned a job to give insights to a user who is applying for a job role of {input_role} and the job description are as follows {input_text}.

# You need to tell the user what parts need modification and what they are.
# """

# sys_prompt3 = f"""
# You are a very advanced ATS software who is very adept in scanning resume against the given role {input_role} and job description: {input_text}.

# You need to follow this sequence and generate the response accordingly:
# 1. Understand the job role and job description
# 2. Find the key words and highlight and match them to the user's resume
# 3. Then calculate an ATS score based on your calculations
# """

# if submit_btn1:
#     if uploaded_file is not None:
#         with st.spinner("Analyzing..."):
#             pdf_content = pdf_upload(uploaded_file)
#             if pdf_content:
#                 response = gemini_response(pdf_content, sys_prompt1)
#                 st.write(response)
#     else:
#         st.write("Please Upload the resume")

# if submit_btn2:
#     if uploaded_file is not None:
#         with st.spinner("Analyzing..."):
#             pdf_content = pdf_upload(uploaded_file)
#             if pdf_content:
#                 response = gemini_response(pdf_content, sys_prompt2)
#                 st.write(response)
#     else:
#         st.write("Please Upload the resume")

# if submit_btn3:
#     if uploaded_file is not None:
#         with st.spinner("Analyzing..."):
#             pdf_content = pdf_upload(uploaded_file)
#             if pdf_content:
#                 response = gemini_response(pdf_content, sys_prompt3)
#                 st.write(response)
#     else:
#         st.write("Please Upload the resume")

# load env variables 
from dotenv import load_dotenv
load_dotenv()

# import packages
import streamlit as st
import os
import io
from PyPDF2 import PdfReader
import google.generativeai as genai

# Configure API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_text_from_pdf(pdf_file):
    """Extract text content from PDF without using images"""
    if pdf_file is not None:
        try:
            pdf = PdfReader(pdf_file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n\n"
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return None
    else:
        raise FileNotFoundError('No File Found')

def gemini_response(text_content, prompt):
    """Send text and prompt to Gemini and get response"""
    # Using text-only model instead of vision model
    model = genai.GenerativeModel('gemini-2.0-flash')
    # Combine resume text with the prompt
    full_prompt = f"""
    RESUME CONTENT:
    {text_content}
    
    INSTRUCTIONS:
    {prompt}
    """
    response = model.generate_content(full_prompt)
    return response.text

# Configuration of Streamlit App
st.set_page_config(page_title="ATS Resume Scanner")
st.header('ATS Resume Scanner')
input_text = st.text_area("Job Description", key="input")
# Input Roles
input_role = st.text_area("Enter the Role You are applying for...", key="role")
uploaded_file = st.file_uploader("Upload Your Resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write('PDF Uploaded Successfully')

submit_btn1 = st.button("Tell me about Resume")
submit_btn2 = st.button("How can I improvise my Skills")
submit_btn3 = st.button("Percentage Match")

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
    if uploaded_file is not None:
        with st.spinner("Analyzing..."):
            text_content = extract_text_from_pdf(uploaded_file)
            if text_content:
                response = gemini_response(text_content, sys_prompt1)
                st.write(response)
            else:
                st.error("Could not extract text from the PDF. Please try another file.")
    else:
        st.write("Please Upload the resume")

if submit_btn2:
    if uploaded_file is not None:
        with st.spinner("Analyzing..."):
            text_content = extract_text_from_pdf(uploaded_file)
            if text_content:
                response = gemini_response(text_content, sys_prompt2)
                st.write(response)
            else:
                st.error("Could not extract text from the PDF. Please try another file.")
    else:
        st.write("Please Upload the resume")

if submit_btn3:
    if uploaded_file is not None:
        with st.spinner("Analyzing..."):
            text_content = extract_text_from_pdf(uploaded_file)
            if text_content:
                response = gemini_response(text_content, sys_prompt3)
                st.write(response)
            else:
                st.error("Could not extract text from the PDF. Please try another file.")
    else:
        st.write("Please Upload the resume")