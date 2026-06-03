from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from extensions import db
from models.interview import Interview
import random

mock_interview = Blueprint("mock_interview", __name__)

QUESTION_BANK = {
    "Full Stack Developer": [
        "What is the difference between frontend and backend development?",
        "Explain what HTML, CSS, and JavaScript are used for.",
        "What is a REST API?",
        "How do you use Git to save changes?",
        "What is responsive web design?",
        "What is database normalization?",
        "Explain authentication and authorization."
    ],
    "Python Developer": [
        "What are lists and tuples in Python?",
        "Explain functions in Python.",
        "What is OOP?",
        "What is exception handling?",
        "What are dictionaries in Python?"
    ],
    "AI Engineer": [
        "What is Machine Learning?",
        "Difference between AI, ML, and Deep Learning.",
        "What is supervised learning?",
        "What is overfitting?",
        "What is a dataset?"
    ],
    "Data Analyst": [
        "What is data cleaning?",
        "What is SQL used for?",
        "What is data visualization?",
        "What is Excel used for in analysis?",
        "What is a dashboard?"
    ]
}


@mock_interview.route("/mock-interview", methods=["GET", "POST"])
@login_required
def mock_interview_page():
    questions = []
    score = None
    feedback = []
    role = ""
    difficulty = ""

    if request.method == "POST":
        role = request.form.get("role")
        difficulty = request.form.get("difficulty")
        action = request.form.get("action")

        if action == "generate":
            questions = random.sample(QUESTION_BANK.get(role, []), 5)

        elif action == "submit":
            questions = request.form.getlist("questions")
            answers = request.form.getlist("answers")

            total = 0

            for i, answer in enumerate(answers):
                words = answer.strip().split()

                if len(words) >= 25:
                    marks = 2
                    msg = "Good answer with enough explanation."
                elif len(words) >= 10:
                    marks = 1
                    msg = "Average answer. Add more examples."
                else:
                    marks = 0
                    msg = "Too short. Explain clearly with points."

                total += marks

                feedback.append({
                    "question": questions[i],
                    "answer": answer,
                    "marks": marks,
                    "message": msg
                })

            score = total

            interview = Interview(
                user_id=current_user.id,
                role=role,
                difficulty=difficulty,
                score=score
            )

            db.session.add(interview)
            db.session.commit()

    return render_template(
        "mock_interview.html",
        questions=questions,
        score=score,
        feedback=feedback,
        role=role,
        difficulty=difficulty
    )


@mock_interview.route("/interview-history")
@login_required
def interview_history():
    interviews = Interview.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Interview.created_at.desc()
    ).all()

    return render_template(
        "interview_history.html",
        interviews=interviews
    )