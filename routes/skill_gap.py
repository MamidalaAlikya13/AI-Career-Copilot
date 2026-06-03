from flask import Blueprint, render_template, request
from flask_login import login_required

skill_gap = Blueprint("skill_gap", __name__)

ROLE_SKILLS = {
    "AI Engineer": [
        "Python", "Machine Learning", "SQL",
        "Deep Learning", "Git"
    ],
    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript",
        "Flask", "SQL", "Git"
    ],
    "Data Analyst": [
        "Excel", "SQL", "Python",
        "Power BI", "Statistics"
    ],
    "Python Developer": [
        "Python", "Flask", "SQL",
        "Git", "REST API"
    ]
}


@skill_gap.route("/skill-gap", methods=["GET", "POST"])
@login_required
def skill_gap_page():

    missing_skills = []
    role = ""

    if request.method == "POST":

        role = request.form.get("role")

        resume_text = request.form.get(
            "resume_text",
            ""
        ).lower()

        required_skills = ROLE_SKILLS.get(role, [])

        missing_skills = [
            skill
            for skill in required_skills
            if skill.lower() not in resume_text
        ]

    return render_template(
        "skill_gap.html",
        role=role,
        missing_skills=missing_skills
    )