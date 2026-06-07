from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from extensions import db
from models.interview import Interview
import random

mock_interview = Blueprint("mock_interview", __name__)


QUESTION_BANK = {
    "Frontend Developer": {
        "Easy": [
            "What is HTML used for?",
            "What is CSS used for?",
            "What is JavaScript?",
            "What is responsive web design?",
            "What is Bootstrap?",
            "What is the difference between id and class in CSS?",
            "What are semantic HTML tags?",
            "What is Flexbox?",
            "What is CSS Grid?",
            "What is the DOM?"
        ],
        "Medium": [
            "Explain event handling in JavaScript.",
            "What is the difference between let, const, and var?",
            "What is API integration in frontend development?",
            "Explain the box model in CSS.",
            "What are media queries?",
            "What is localStorage in JavaScript?",
            "What is form validation?",
            "Explain promises in JavaScript.",
            "What is React used for?",
            "What are components in React?"
        ],
        "Hard": [
            "How do you optimize frontend performance?",
            "Explain virtual DOM.",
            "How do you handle state management in frontend apps?",
            "Explain accessibility in web design.",
            "How do you secure frontend applications?",
            "What is lazy loading?",
            "Explain code splitting.",
            "How do you debug frontend performance issues?",
            "What is server-side rendering?",
            "Explain progressive web apps."
        ]
    },

    "Backend Developer": {
        "Easy": [
            "What is backend development?",
            "What is a database?",
            "What is an API?",
            "What is authentication?",
            "What is authorization?",
            "What is SQL?",
            "What is Flask?",
            "What is a server?",
            "What is CRUD?",
            "What is HTTP?"
        ],
        "Medium": [
            "Explain REST API.",
            "What is JWT authentication?",
            "What is database normalization?",
            "What is middleware?",
            "Explain request and response cycle.",
            "What are status codes?",
            "What is ORM?",
            "Explain sessions and cookies.",
            "What is API validation?",
            "What is pagination?"
        ],
        "Hard": [
            "How do you design scalable backend systems?",
            "How do you secure APIs?",
            "Explain rate limiting.",
            "What is caching?",
            "Explain database indexing.",
            "How do you handle concurrent requests?",
            "What is microservices architecture?",
            "How do you monitor backend performance?",
            "Explain load balancing.",
            "How do you handle production errors?"
        ]
    },

    "Full Stack Developer": {
        "Easy": [
            "What is the difference between frontend and backend development?",
            "Explain what HTML, CSS, and JavaScript are used for.",
            "What is a REST API?",
            "How do you use Git to save changes?",
            "What is responsive web design?",
            "What is database normalization?",
            "Explain authentication and authorization.",
            "What is Bootstrap?",
            "What is Flask?",
            "What is SQLite?"
        ],
        "Medium": [
            "How does a frontend communicate with backend?",
            "Explain CRUD operations with example.",
            "How do login and register systems work?",
            "What is the role of SQLAlchemy?",
            "Explain client-server architecture.",
            "What is form validation?",
            "What are templates in Flask?",
            "How do you deploy a Flask app?",
            "What is environment variable?",
            "How do you protect routes?"
        ],
        "Hard": [
            "How would you design a scalable full-stack application?",
            "How do you secure user authentication?",
            "Explain API error handling.",
            "How do you optimize database queries?",
            "How do you structure a large Flask project?",
            "What is CI/CD?",
            "How do you handle file uploads securely?",
            "Explain session management.",
            "How do you debug production issues?",
            "How do you design role-based access control?"
        ]
    },

    "Python Developer": {
        "Easy": [
            "What are lists and tuples in Python?",
            "Explain functions in Python.",
            "What is OOP?",
            "What is exception handling?",
            "What are dictionaries in Python?",
            "What is a loop?",
            "What is a module?",
            "What is a package?",
            "What is indentation in Python?",
            "What is type casting?"
        ],
        "Medium": [
            "Explain decorators in Python.",
            "What are *args and **kwargs?",
            "Explain list comprehension.",
            "What is file handling?",
            "What is virtual environment?",
            "What is lambda function?",
            "Explain inheritance.",
            "What is polymorphism?",
            "What are generators?",
            "What is pip?"
        ],
        "Hard": [
            "Explain memory management in Python.",
            "What is GIL?",
            "Explain multithreading vs multiprocessing.",
            "How do you optimize Python code?",
            "What are context managers?",
            "Explain dependency management.",
            "How do you handle large files in Python?",
            "What is asynchronous programming?",
            "Explain unit testing in Python.",
            "How do you package a Python project?"
        ]
    },

    "AI Engineer": {
        "Easy": [
            "What is Artificial Intelligence?",
            "What is Machine Learning?",
            "Difference between AI, ML, and Deep Learning.",
            "What is a dataset?",
            "What is supervised learning?",
            "What is unsupervised learning?",
            "What is training data?",
            "What is testing data?",
            "What is model accuracy?",
            "What is classification?"
        ],
        "Medium": [
            "What is overfitting?",
            "What is underfitting?",
            "Explain feature engineering.",
            "What is model evaluation?",
            "What is confusion matrix?",
            "What is regression?",
            "What is neural network?",
            "What is data preprocessing?",
            "What is hyperparameter tuning?",
            "What is cross-validation?"
        ],
        "Hard": [
            "How do you deploy a machine learning model?",
            "Explain bias-variance tradeoff.",
            "How do you handle imbalanced data?",
            "What is transfer learning?",
            "Explain CNN and RNN.",
            "What is MLOps?",
            "How do you monitor ML models in production?",
            "What is model drift?",
            "How do you improve model performance?",
            "Explain end-to-end AI system design."
        ]
    },

    "Data Analyst": {
        "Easy": [
            "What is data cleaning?",
            "What is SQL used for?",
            "What is data visualization?",
            "What is Excel used for in analysis?",
            "What is a dashboard?",
            "What is a chart?",
            "What is mean?",
            "What is median?",
            "What is a filter?",
            "What is sorting?"
        ],
        "Medium": [
            "Explain joins in SQL.",
            "What is pivot table?",
            "What is data storytelling?",
            "What is missing value handling?",
            "What is Power BI?",
            "What is exploratory data analysis?",
            "Explain group by in SQL.",
            "What is correlation?",
            "What are KPIs?",
            "How do you clean duplicate data?"
        ],
        "Hard": [
            "How do you design an analytics dashboard?",
            "Explain cohort analysis.",
            "How do you identify business insights?",
            "How do you handle large datasets?",
            "What is data modeling?",
            "Explain statistical significance.",
            "How do you validate analysis results?",
            "How do you communicate insights to stakeholders?",
            "What is ETL?",
            "How do you automate reporting?"
        ]
    },

    "Software Engineer": {
        "Easy": [
            "What is software engineering?",
            "What is SDLC?",
            "What is debugging?",
            "What is version control?",
            "What is Git?",
            "What is OOP?",
            "What is a database?",
            "What is API?",
            "What is testing?",
            "What is deployment?"
        ],
        "Medium": [
            "Explain Agile methodology.",
            "What are design patterns?",
            "What is unit testing?",
            "What is clean code?",
            "What is code review?",
            "Explain MVC architecture.",
            "What is REST?",
            "What is database indexing?",
            "What is exception handling?",
            "What is CI/CD?"
        ],
        "Hard": [
            "How do you design scalable software?",
            "Explain system design basics.",
            "How do you handle production failures?",
            "What is load balancing?",
            "What is caching?",
            "Explain distributed systems basics.",
            "How do you improve code maintainability?",
            "What is technical debt?",
            "How do you design secure applications?",
            "How do you estimate software projects?"
        ]
    }
}


def get_questions(role, difficulty):
    role_questions = QUESTION_BANK.get(role)

    if not role_questions:
        role_questions = QUESTION_BANK["Software Engineer"]

    questions = role_questions.get(difficulty, role_questions["Easy"])

    count = min(5, len(questions))

    return random.sample(questions, count)


def evaluate_answer(answer, difficulty):
    words = answer.strip().split()
    word_count = len(words)

    if difficulty == "Easy":
        if word_count >= 25:
            return 2, "Good answer. You explained the concept clearly."
        elif word_count >= 10:
            return 1, "Average answer. Add one example for better clarity."
        else:
            return 0, "Too short. Explain the concept with at least 2-3 points."

    if difficulty == "Medium":
        if word_count >= 35:
            return 2, "Strong answer. Good detail and explanation."
        elif word_count >= 18:
            return 1, "Average answer. Add examples, use cases, or steps."
        else:
            return 0, "Too short for medium level. Add more technical depth."

    if difficulty == "Hard":
        if word_count >= 50:
            return 2, "Good hard-level answer. Improve with architecture or real-world example."
        elif word_count >= 25:
            return 1, "Decent attempt. Add deeper explanation and trade-offs."
        else:
            return 0, "Insufficient for hard level. Explain deeply with examples."

    return 0, "Unable to evaluate answer."


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
            questions = get_questions(role, difficulty)

        elif action == "submit":
            questions = request.form.getlist("questions")
            answers = request.form.getlist("answers")

            total = 0

            for i, answer in enumerate(answers):
                marks, msg = evaluate_answer(answer, difficulty)
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