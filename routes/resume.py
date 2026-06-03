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
    "Algorithms", "Database", "Projects", "Internship"
]

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

    readiness_score = min(100, ats_score + 10 if "Projects" in found else ats_score)

    recommendations = []

    if "Git" in missing:
        recommendations.append("Add Git/GitHub experience in your resume.")
    if "Projects" in missing:
        recommendations.append("Add at least 2 strong projects with tech stack and features.")
    if "SQL" in missing:
        recommendations.append("Add SQL/database skills.")
    if "Internship" in missing:
        recommendations.append("Add internship, certification, or virtual experience.")
    if ats_score < 60:
        recommendations.append("Improve technical keywords and project descriptions.")

    if not recommendations:
        recommendations.append("Your resume has good technical coverage. Improve formatting and impact points.")

    return found, missing, ats_score, readiness_score, recommendations

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

        uploads_dir = os.path.join(current_app.root_path, "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        save_path = os.path.join(uploads_dir, filename)
        file.save(save_path)

        extracted_text = extract_pdf_text(save_path)

        found, missing, ats_score, readiness_score, recommendations = analyze_resume(extracted_text)

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
            resume=resume_obj
        )

    return render_template("upload_resume.html")