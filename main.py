from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import fitz
import re

app = FastAPI(title="AI Resume Updated")


def extract_resume_text(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text


def extract_candidate_details(text):

    email = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    phone = re.search(
        r'(\+?\d[\d\s-]{8,}\d)',
        text
    )

    skills_list = [
        "Python",
        "Java",
        "C++",
        "JavaScript",
        "React",
        "FastAPI",
        "Django",
        "Machine Learning",
        "Deep Learning",
        "Generative AI",
        "LLM",
        "RAG",
        "LangChain",
        "LangGraph",
        "SQL",
        "PostgreSQL",
        "Docker",
        "Git",
        "AWS",
        "Qdrant"
    ]

    found_skills = []

    for skill in skills_list:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    return {
        "email": email.group(0) if email else "Not found",
        "phone": phone.group(0) if phone else "Not found",
        "skills": found_skills,
        "education": extract_section(
            text,
            ["education", "qualification"]
        ),
        "experience": extract_section(
            text,
            ["experience", "work experience"]
        )
    }


def extract_section(text, keywords):

    lines = text.splitlines()

    for i, line in enumerate(lines):

        if any(
            keyword in line.lower()
            for keyword in keywords
        ):

            return "\n".join(
                lines[i:i + 6]
            )

    return "Not clearly identified"


def skill_gap_analysis(
    resume_skills,
    job_description
):

    required_skills = [
        "Python",
        "FastAPI",
        "PostgreSQL",
        "RAG",
        "Qdrant",
        "LangGraph",
        "LLM",
        "Git"
    ]

    resume_lower = [
        skill.lower()
        for skill in resume_skills
    ]

    jd_text = job_description.lower()

    matched = []
    missing = []

    for skill in required_skills:

        if skill.lower() in jd_text:

            if skill.lower() in resume_lower:
                matched.append(skill)
            else:
                missing.append(skill)

    total = len(matched) + len(missing)

    score = 0

    if total > 0:
        score = round(
            len(matched) / total * 100
        )

    return {
        "matched_skills": matched,
        "skill_gaps": missing,
        "match_score": score
    }


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>AI Resume Updated</title>

        <style>

            body {
                font-family: Arial;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }

            textarea {
                width: 100%;
                height: 180px;
                padding: 10px;
            }

            input {
                margin: 10px 0;
                padding: 10px;
            }

            button {
                padding: 12px 20px;
                cursor: pointer;
            }

            .box {
                border: 1px solid #ddd;
                padding: 20px;
                margin: 20px 0;
                border-radius: 10px;
            }

        </style>

    </head>

    <body>

        <h1>AI Resume Updated</h1>

        <div class="box">

            <h2>Resume Analysis</h2>

            <form
                action="/analyze"
                method="post"
                enctype="multipart/form-data"
            >

                <input
                    type="file"
                    name="resume"
                    accept=".pdf"
                    required
                >

                <h3>Job Description</h3>

                <textarea
                    name="job_description"
                    placeholder="Paste Job Description here..."
                    required
                ></textarea>

                <br><br>

                <button type="submit">
                    Analyze Resume
                </button>

            </form>

        </div>

    </body>

    </html>
    """


@app.post(
    "/analyze",
    response_class=HTMLResponse
)
async def analyze(

    resume: UploadFile = File(...),

    job_description: str = Form(...)

):

    pdf_bytes = await resume.read()

    resume_text = extract_resume_text(
        pdf_bytes
    )

    candidate = extract_candidate_details(
        resume_text
    )

    analysis = skill_gap_analysis(
        candidate["skills"],
        job_description
    )

    skills = (
        ", ".join(candidate["skills"])
        if candidate["skills"]
        else "No recognized skills found"
    )

    matched = (
        ", ".join(
            analysis["matched_skills"]
        )
        if analysis["matched_skills"]
        else "None"
    )

    gaps = (
        ", ".join(
            analysis["skill_gaps"]
        )
        if analysis["skill_gaps"]
        else "No major gaps identified"
    )

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Resume Assessment Report</title>

        <style>

            body {{
                font-family: Arial;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }}

            .box {{
                border: 1px solid #ddd;
                padding: 20px;
                margin: 20px 0;
                border-radius: 10px;
            }}

        </style>

    </head>

    <body>

        <h1>Candidate Assessment Report</h1>

        <div class="box">

            <h2>Candidate Details</h2>

            <p>
                <b>Email:</b>
                {candidate["email"]}
            </p>

            <p>
                <b>Phone:</b>
                {candidate["phone"]}
            </p>

            <p>
                <b>Education:</b><br>
                {candidate["education"]}
            </p>

            <p>
                <b>Experience:</b><br>
                {candidate["experience"]}
            </p>

        </div>

        <div class="box">

            <h2>Extracted Skills</h2>

            <p>
                {skills}
            </p>

        </div>

        <div class="box">

            <h2>Skill Gap Analysis</h2>

            <h3>
                Match Score:
                {analysis["match_score"]}%
            </h3>

            <p>
                <b>Matched Skills:</b>
                {matched}
            </p>

            <p>
                <b>Skill Gaps:</b>
                {gaps}
            </p>

        </div>

        <a href="/">
            Analyze another resume
        </a>

    </body>

    </html>
    """


@app.get("/health")
def health():

    return {
        "status": "running",
        "project": "AI Resume Updated"
    }