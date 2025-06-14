# Lucky SaaS Final Submission Build 🚀

from dotenv import load_dotenv
load_dotenv()

import os
import io
import json
import fitz
import streamlit as st
import google.generativeai as genai
import re
from docx import Document
import requests
import streamlit_lottie as st_lottie
from requests.exceptions import RequestException
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
import base64

# Configure Gemini Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Global Config
st.set_page_config(page_title="Anveshan : AI Resume Builder", page_icon="💼", layout="wide")

# Session State Init
if 'version_history' not in st.session_state:
    st.session_state.version_history = []

# Lottie Loader
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except RequestException:
        return None

# File Parser
def parse_file(uploaded_file):
    try:
        file_ext = uploaded_file.name.split(".")[-1].lower()
        if file_ext == "pdf":
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            text = "".join(page.get_text() for page in doc)
        elif file_ext == "docx":
            document = Document(uploaded_file)
            text = "\n".join([para.text for para in document.paragraphs])
        elif file_ext == "txt":
            text = uploaded_file.read().decode("utf-8")
        else:
            raise ValueError("Unsupported file format.")
        return text
    except Exception as e:
        st.error(f"File parsing error: {str(e)}")
        return None

# Contact Extractor
def extract_contact_info(resume_text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}'
    linkedin_pattern = r'(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+'
    email = re.search(email_pattern, resume_text)
    phone = re.search(phone_pattern, resume_text)
    linkedin = re.search(linkedin_pattern, resume_text)
    lines = resume_text.strip().split('\n')
    name = next((line.strip() for line in lines if line.strip()), "Not found")
    return {
        "Name": name,
        "Email": email.group() if email else "Not found",
        "Phone": phone.group() if phone else "Not found",
        "LinkedIn": linkedin.group() if linkedin else "Not found"
    }

# Gemini JSON Extractor
def extract_json(response_text):
    try:
        json_pattern = re.compile(r"\{.*\}", re.DOTALL)
        match = json_pattern.search(response_text)
        if match:
            clean_json = match.group()
            return json.loads(clean_json)
        else:
            raise ValueError("No valid JSON found.")
    except Exception as e:
        st.error(f"⚠ Gemini returned invalid JSON: {e}")
        return None

# Gemini ATS Analyzer
def analyze_resume(resume_text, job_description, role="generic"):
    model = genai.GenerativeModel("gemini-1.5-flash")

    task = f"""
You are an advanced ATS resume analyzer specialized for role: {role}.
Strictly return JSON output only. DO NOT add any explanations.

Task:
- Grade formatting, completeness, keyword relevance, clarity.
- Perform tone analysis.
- Output strictly in JSON format like:

{{
  "overall_score": 0-100,
  "tone": "professional | friendly | weak | informal",
  "missing_keywords": ["keyword1", "keyword2"],
  "section_scores": {{
    "Education": 0-100,
    "Experience": 0-100,
    "Skills": 0-100,
    "Formatting": 0-100,
    "Clarity": 0-100
  }},
  "suggestions": ["actionable suggestion 1", "actionable suggestion 2"]
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

    response = model.generate_content(task)
    return extract_json(response.text)

# ----------------- Resume Builder ------------------

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return re.match(r"^[\+]?[\d\s-]{7,15}$", phone)

def validate_linkedin(linkedin):
    return "linkedin.com/in/" in linkedin

def build_resume():
    st.subheader("🎯 Build Your Resume")
    with st.form("resume_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        linkedin = st.text_input("LinkedIn URL")
        education = st.text_area("Education")
        experience = st.text_area("Experience")
        skills = st.text_area("Skills (comma-separated)")
        projects = st.text_area("Projects")
        summary = st.text_area("Professional Summary")
        submit = st.form_submit_button("✅ Generate Resume")

    if submit:
        errors = []
        if not full_name: errors.append("Name required.")
        if not validate_email(email): errors.append("Invalid email.")
        if not validate_phone(phone): errors.append("Invalid phone.")
        if not validate_linkedin(linkedin): errors.append("Invalid LinkedIn URL.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            resume_content = f"""
{full_name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}

Summary:
{summary}

Education:
{education}

Experience:
{experience}

Projects:
{projects}

Skills:
{skills}
"""
            st.success("🎉 Resume Generated Successfully!")
            st.download_button("Download Resume as TXT", resume_content, file_name="resume.txt")
            return resume_content
    return None

# ----------------- Main UI ------------------

selected = option_menu("Anveshan 🚀", ["🏠 Home", "📊 Analyze Resume", "📝 Build Resume", "📈 Version History"], 
                       icons=["house", "graph-up", "file-earmark-person", "clock-history"], default_index=0)

# Lottie Header Animation (optional if you want to download lottie json to assets/)
lottie_url = "https://assets10.lottiefiles.com/packages/lf20_kyu7xb1v.json"
header_lottie = load_lottie_url(lottie_url)
if header_lottie:
    st_lottie.st_lottie(header_lottie, speed=1, width=700, height=300)

# HOME
if selected == "🏠 Home":
    st.title("💼 AI Resume Analyzer & Builder")
    st.write("""
Welcome to Anveshan — Build, Analyze & Improve your Resume using Generative AI 🔥
- Multi-format resume upload (PDF/DOCX/TXT)
- Role-specific ATS Analyzer
- Smart Feedback & Keyword Suggestions
- Resume Builder with Validation
- Version History to track your improvements
""")

# ANALYZER
if selected == "📊 Analyze Resume":
    st.header("📊 Upload & Analyze Your Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    job_description = st.text_area("Paste Job Description:")
    role = st.selectbox("Select Role for Analysis", ["generic", "developer", "data scientist", "designer", "product manager"])

    if st.button("🚀 Analyze Now"):
        if uploaded_file and job_description:
            resume_text = parse_file(uploaded_file)
            if resume_text:
                contact_info = extract_contact_info(resume_text)
                with st.spinner("Analyzing with Gemini..."):
                    ai_result = analyze_resume(resume_text, job_description, role)
                    if ai_result:
                        st.success("✅ Resume Analyzed Successfully!")

                        st.subheader("Contact Information Extracted:")
                        st.write(contact_info)

                        st.subheader("Overall Score:")
                        st.progress(ai_result['overall_score'])
                        st.write(f"Score: {ai_result['overall_score']} / 100")

                        st.subheader("Tone:")
                        st.write(ai_result['tone'])

                        st.subheader("Section Scores:")
                        for sec, sc in ai_result['section_scores'].items():
                            st.write(f"**{sec}**: {sc}/100")

                        st.subheader("Missing Keywords:")
                        st.write(", ".join(ai_result['missing_keywords']))

                        st.subheader("Suggestions:")
                        for sug in ai_result['suggestions']:
                            st.write(f"👉 {sug}")

                        if ai_result['missing_keywords']:
                            st.subheader("🔎 Missing Keywords WordCloud")
                            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(ai_result['missing_keywords']))
                            plt.imshow(wordcloud, interpolation='bilinear')
                            plt.axis("off")
                            st.pyplot(plt)

                        st.session_state.version_history.append(ai_result)
        else:
            st.warning("Please upload resume and job description.")

# BUILDER
if selected == "📝 Build Resume":
    result = build_resume()

# VERSION HISTORY
if selected == "📈 Version History":
    st.header("🕰️ Resume Version History")
    if not st.session_state.version_history:
        st.info("No resume analysis done yet.")
    else:
        for i, version in enumerate(st.session_state.version_history, 1):
            with st.expander(f"Version {i} - Score: {version['overall_score']}"):
                st.write(f"Tone: {version['tone']}")
                st.write(f"Missing Keywords: {version['missing_keywords']}")
                st.write("Suggestions:")
                for sug in version['suggestions']:
                    st.write(f"👉 {sug}")
