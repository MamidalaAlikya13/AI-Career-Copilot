import os
from flask import Blueprint, render_template, request, redirect, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from models.resume import Resume
from PyPDF2 import PdfReader

resume = Blueprint("resume", __name__)

ALLOWED_EXTENSIONS = {"pdf"}

KEYWORDS = [
    "Python", "SQL", "Flask", "Git", "Machine Learning",
    "REST API", "HTML", "CSS", "JavaScript", "Data Structures",
    "Algorithms", "Database", "Projects", "Internship",
    "API", "GitHub", "Deployment", "Problem Solving"
]

ROLE_KEYWORDS = {
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "SQL", "Model Deployment"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "Flask", "SQL", "REST API", "Git"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Responsive Design"],
    "Backend Developer": ["Python", "Flask", "SQL", "REST API", "Authentication"],
    "Data Analyst": ["Excel", "SQL", "Python", "Pandas", "Power BI"],
    "Software Engineer": ["Data Structures", "Algorithms", "OOP", "Git", "Database"]
}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_pdf_text(path):
    text = ""

    try:
        reader = PdfReader(path)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception:
        text = ""

    return text


def analyze_resume(text):
    lower_text = text.lower()

    found = []
    missing = []

    for skill in KEYWORDS:
        if skill.lower() in lower_text:
            found.append(skill)
        else:
            missing.append(skill)

    ats_score = int((len(found) / len(KEYWORDS)) * 100)

    if "Projects" in found or "projects" in lower_text:
        readiness_score = min(100, ats_score + 10)
    else:
        readiness_score = ats_score

    recommendations = generate_recommendations(found, missing, ats_score, lower_text)
    strengths = generate_strengths(found, lower_text)
    weaknesses = generate_weaknesses(missing, lower_text)
    recommended_roles = recommend_roles(lower_text)
    ai_summary = generate_ai_summary(ats_score, readiness_score, found, missing, recommended_roles)

    return (
        found,
        missing,
        ats_score,
        readiness_score,
        recommendations,
        strengths,
        weaknesses,
        recommended_roles,
        ai_summary
    )


def generate_recommendations(found, missing, ats_score, lower_text):
    recommendations = []

    if "Git" in missing and "GitHub" in missing:
        recommendations.append("Add Git and GitHub links to show version control experience.")

    if "Projects" in missing and "project" not in lower_text:
        recommendations.append("Add at least 2 strong projects with tech stack, features, and deployment links.")

    if "SQL" in missing:
        recommendations.append("Add SQL/database skills if you are targeting software or data roles.")

    if "REST API" in missing and "API" in missing:
        recommendations.append("Mention REST API development or API integration experience.")

    if "Internship" in missing:
        recommendations.append("Add internship, virtual internship, certification, or workshop experience.")

    if "Deployment" in missing:
        recommendations.append("Add deployed project links such as Render, Vercel, Netlify, or GitHub Pages.")

    if ats_score < 50:
        recommendations.append("Improve resume keywords, project descriptions, and technical skills section.")

    if ats_score >= 70:
        recommendations.append("Your resume has good keyword coverage. Improve impact points and measurable outcomes.")

    if not recommendations:
        recommendations.append("Improve formatting, add measurable achievements, and include role-specific keywords.")

    return recommendations


def generate_strengths(found, lower_text):
    strengths = []

    if "Python" in found:
        strengths.append("Python skill is present, which is useful for software, AI, and data roles.")

    if "Projects" in found or "project" in lower_text:
        strengths.append("Projects are mentioned, which improves practical credibility.")

    if "Git" in found or "GitHub" in found:
        strengths.append("Git/GitHub presence shows version control awareness.")

    if "Machine Learning" in found:
        strengths.append("Machine Learning keyword supports AI/ML career direction.")

    if "Internship" in found or "internship" in lower_text:
        strengths.append("Internship experience adds real-world exposure.")

    if not strengths:
        strengths.append("Resume has basic content, but needs stronger technical and project-based evidence.")

    return strengths


def generate_weaknesses(missing, lower_text):
    weaknesses = []

    if "Projects" in missing and "project" not in lower_text:
        weaknesses.append("Projects section appears weak or missing.")

    if "Git" in missing and "GitHub" in missing:
        weaknesses.append("Git/GitHub proof is missing.")

    if "SQL" in missing:
        weaknesses.append("Database skill visibility is low.")

    if "REST API" in missing and "API" in missing:
        weaknesses.append("API development or integration experience is not clearly visible.")

    if "Deployment" in missing:
        weaknesses.append("Live project deployment links are missing.")

    if not weaknesses:
        weaknesses.append("No major weakness detected from tracked keywords. Improve clarity and measurable results.")

    return weaknesses


def recommend_roles(lower_text):
    scores = {}

    for role, keywords in ROLE_KEYWORDS.items():
        count = 0

        for keyword in keywords:
            if keyword.lower() in lower_text:
                count += 1

        scores[role] = count

    sorted_roles = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    recommended = [
        role
        for role, score in sorted_roles
        if score > 0
    ]

    if not recommended:
        recommended = ["Software Engineer", "Python Developer", "Full Stack Developer"]

    return recommended[:3]


def generate_ai_summary(ats_score, readiness_score, found, missing, recommended_roles):
    if ats_score >= 75:
        level = "strong"
    elif ats_score >= 50:
        level = "moderate"
    else:
        level = "needs improvement"

    return f"""
AI Resume Expert Summary:

Your resume currently has a {level} technical keyword profile.

ATS Simulation Score:
{ats_score}/100

Placement Readiness:
{readiness_score}/100

Best Matching Roles:
{", ".join(recommended_roles)}

Overall Verdict:
This is an AI-assisted resume analysis, not a guaranteed real ATS result. 
Use it as guidance to improve keywords, projects, skills, and role alignment.
"""


@resume.route("/upload_resume", methods=["GET", "POST"])
@login_required
def upload_resume():
    if request.method == "POST":

        if "file" not in request.files:
            flash("No file uploaded", "danger")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file", "danger")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Only PDF files are allowed", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)

        uploads_dir = os.path.join(
            current_app.root_path,
            "uploads"
        )

        os.makedirs(uploads_dir, exist_ok=True)

        save_path = os.path.join(
            uploads_dir,
            filename
        )

        file.save(save_path)

        extracted_text = extract_pdf_text(save_path)

        (
            found,
            missing,
            ats_score,
            readiness_score,
            recommendations,
            strengths,
            weaknesses,
            recommended_roles,
            ai_summary
        ) = analyze_resume(extracted_text)

        resume_obj = Resume(
            user_id=current_user.id,
            filename=filename,
            ats_score=ats_score,
            extracted_text=extracted_text
        )

        db.session.add(resume_obj)
        db.session.commit()

        return render_template(
            "resume_result.html",
            score=ats_score,
            readiness_score=readiness_score,
            found=found,
            missing=missing,
            recommendations=recommendations,
            strengths=strengths,
            weaknesses=weaknesses,
            recommended_roles=recommended_roles,
            ai_summary=ai_summary,
            resume=resume_obj
        )

    return render_template("upload_resume.html")