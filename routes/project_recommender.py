from flask import Blueprint, render_template, request
from flask_login import login_required

project_recommender = Blueprint("project_recommender", __name__)

PROJECTS = {
    "AI Engineer": [
        "AI Resume Analyzer",
        "AI Interview Preparation Bot",
        "Traffic Prediction Dashboard",
        "Fake News Detection System"
    ],
    "Full Stack Developer": [
        "Personal Finance Tracker",
        "Student Placement Portal",
        "Online Course Platform",
        "Task Management Web App"
    ],
    "Data Analyst": [
        "Sales Dashboard",
        "Student Performance Analysis",
        "COVID Data Visualization",
        "Customer Churn Analysis"
    ],
    "Python Developer": [
        "Expense Tracker",
        "Quiz Application",
        "File Organizer",
        "Library Management System"
    ]
}

@project_recommender.route("/project-recommender", methods=["GET", "POST"])
@login_required
def recommender():
    selected_goal = ""
    recommendations = []

    if request.method == "POST":
        selected_goal = request.form.get("goal")
        recommendations = PROJECTS.get(selected_goal, [])

    return render_template(
        "project_recommender.html",
        selected_goal=selected_goal,
        recommendations=recommendations
    )