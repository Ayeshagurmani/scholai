import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load API key from .env file
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load our real scholarship database
with open("scholarships.json", "r") as f:
    SCHOLARSHIP_DB = json.load(f)["scholarships"]


def read_cv(uploaded_file) -> str:
    """
    WHAT: Reads the uploaded CV file and extracts raw text
    WHY: AI can only read text, not PDF/Word files directly
    so we convert the file to plain text first
    """
    import fitz  # pymupdf
    import io

    if uploaded_file.name.endswith(".pdf"):
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    else:
        from docx import Document
        doc = Document(io.BytesIO(uploaded_file.read()))
        return "\n".join([para.text for para in doc.paragraphs])


def analyze_cv(cv_text: str) -> dict:
    """
    WHAT: Sends CV text to AI and gets back structured profile
    WHY: We need organized data (skills, GPA, experience)
    to match against scholarship requirements
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are an expert CV analyzer for Pakistani students.
                Extract information and return ONLY a JSON object with these exact keys:
                - name: full name (string)
                - email: email address (string)
                - education_level: one of "Bachelors", "Masters", "PhD" (string)
                - gpa: GPA as a number out of 4.0, estimate if not mentioned (number)
                - experience_years: years of work experience as a number (number)
                - skills: list of top 6 skills (list)
                - field_of_study: their main field e.g. Computer Science (string)
                - english_test: IELTS or TOEFL score if mentioned, else "Not mentioned" (string)
                - achievements: list of up to 3 key achievements (list)
                - summary: 2 sentence professional summary (string)
                Return only JSON, no markdown, no extra text."""
            },
            {
                "role": "user",
                "content": f"Analyze this CV:\n\n{cv_text}"
            }
        ]
    )
    return json.loads(response.choices[0].message.content)


def match_scholarships(profile: dict) -> list:
    """
    WHAT: Matches the student profile against our scholarship database
    WHY: This is the CORE agent task — reasoning about fit
    between a person and opportunities based on multiple factors.
    This is what makes it an agent — it reasons, not just searches.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": """You are a scholarship matching expert for Pakistani students.
                You will be given a student profile and a list of scholarships.
                Analyze each scholarship carefully and return ONLY a JSON object with 
                a key "matches" containing a list of ALL scholarships with these fields:
                - name: scholarship name
                - country: country
                - match_score: percentage 0-100 based on how well student qualifies
                - why_match: one sentence explaining the match
                - gaps: list of specific things student needs to improve
                - eligible: true or false based on basic requirements
                - priority: "High", "Medium" or "Low"
                Sort by match_score highest first.
                Return only JSON, no markdown."""
            },
            {
                "role": "user",
                "content": f"""Student Profile:
{json.dumps(profile, indent=2)}

Available Scholarships:
{json.dumps(SCHOLARSHIP_DB, indent=2)}

Match this student to these scholarships."""
            }
        ]
    )
    result = json.loads(response.choices[0].message.content)
    return result["matches"]


def generate_sop(profile: dict, scholarship: dict) -> str:
    """
    WHAT: Writes a personalized Statement of Purpose
    WHY: This is the agent TAKING ACTION — producing something
    useful and personalized, not just finding information.
    Every SOP is unique to the student + scholarship combination.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert scholarship application writer 
                specializing in Pakistani student applications.
                Write a compelling Statement of Purpose.
                Rules:
                - Address the specific scholarship and country
                - Use ONLY real information from the student profile
                - Write exactly 4 paragraphs:
                  1. Who you are and your background
                  2. Your academic and professional achievements  
                  3. Why this specific scholarship and country
                  4. Your future goals and how this helps Pakistan
                - Professional, genuine tone
                - No generic phrases like "I am writing to apply"
                - Maximum 400 words"""
            },
            {
                "role": "user",
                "content": f"""Write an SOP for {profile['name']} 
applying to {scholarship['name']} in {scholarship['country']}.

Student Profile:
{json.dumps(profile, indent=2)}"""
            }
        ]
    )
    return response.choices[0].message.content