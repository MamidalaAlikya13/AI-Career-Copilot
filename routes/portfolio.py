from flask import Blueprint, render_template, request
from flask_login import login_required

portfolio = Blueprint("portfolio", __name__)


@portfolio.route("/portfolio-generator", methods=["GET", "POST"])
@login_required
def portfolio_generator():
    if request.method == "POST":

        skills_text = request.form.get("skills", "")

        skills = [
            skill.strip()
            for skill in skills_text.split(",")
            if skill.strip()
        ]

        data = {
            "name": request.form.get("name"),
            "title": request.form.get("title"),
            "about": request.form.get("about"),
            "skills": skills,
            "projects": request.form.get("projects"),
            "education": request.form.get("education"),
            "certificates": request.form.get("certificates"),
            "email": request.form.get("email"),
            "github": request.form.get("github"),
            "linkedin": request.form.get("linkedin")
        }

        return render_template(
            "portfolio_preview.html",
            data=data
        )

    return render_template("portfolio_generator.html")