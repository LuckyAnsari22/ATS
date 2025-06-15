✅ Anveshan: AI-Powered Resume Analyzer & Builder
🌟 Project Overview
Anveshan is a next-gen AI-powered resume analyzer & builder that helps job seekers elevate their resumes to meet modern hiring standards.

Instantly analyze resumes with ATS-based AI scoring.

Generate highly personalized, actionable feedback.

Build fully validated resumes inside the app itself.

Maintain version history to track improvements.

Ensure resumes are aligned with job descriptions to improve selection chances.

🔧 Key Features & Technologies
🔥 Core Features
📄 Multi-Format Support: PDF, DOCX, TXT uploads.

🎯 Role-Specific ATS Analyzer: Developer, Data Scientist, Designer, etc.

💡 AI-Powered Feedback: Gemini 1.5-powered suggestions.

📊 Section-Wise Scoring: Education, Experience, Skills, Formatting, Clarity.

🔍 Keyword Gap Analysis: Identify missing keywords.

🎨 Visual Insights: WordCloud visualization for better UX.

🏗 Interactive Resume Builder: Live validation for every field.

🕰 Version History: Save & compare resume versions.

⚙ Error Handling: Robust validations for fields like email, phone, LinkedIn, etc.

🛠 Tech Stack
Python 3

Streamlit

Google Gemini API (generativeai)

PyMuPDF (pdf parsing)

python-docx

WordCloud

Matplotlib

streamlit-lottie

streamlit-option-menu

dotenv

requests

🚀 Live Demo
👉 Deployed Application https://atslucky.streamlit.app/



⚙️ Setup Instructions
1️⃣ Clone the repository:
bash
Copy
Edit
git clone https://github.com/LuckyAnsari22/ATS

2️⃣ Install dependencies:
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Add your Google Gemini API key:
Create a .env file:

bash
Copy
Edit
GOOGLE_API_KEY=your_google_gemini_api_key_here
✅ Note: In production (Streamlit Cloud), you will use Secrets Manager.

4️⃣ Run the app locally:
bash
Copy
Edit
streamlit run app.py
🎯 Deployment Guide (Streamlit Cloud)
Push your repo to GitHub.

Login at https://streamlit.io/cloud.

Connect your GitHub repo.

Add your GOOGLE_API_KEY via Secrets.

Deploy ✅

👨‍⚖️ Hackathon Judges Summary
Demonstrates:

LLM prompt engineering

Document parsing (PDF, DOCX, TXT)

End-to-end resume lifecycle

AI-powered resume builder

Full error handling & user-friendly validations

Beautiful interactive UI

Built with ❤️ by Lucky Ansari 🚀
