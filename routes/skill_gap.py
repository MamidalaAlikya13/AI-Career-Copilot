from flask import Blueprint, render_template, request
from flask_login import login_required

skill_gap = Blueprint("skill_gap", __name__)

ROLE_SKILLS = {
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "SQL", "Git", "Model Deployment", "Statistics"
    ],

    "Machine Learning Engineer": [
        "Python", "Scikit-learn", "Pandas",
        "Feature Engineering", "Model Evaluation", "SQL",
        "MLOps", "Git"
    ],

    "Data Scientist": [
        "Python", "Statistics", "Pandas",
        "Machine Learning", "SQL", "Data Visualization",
        "Model Evaluation"
    ],

    "Data Analyst": [
        "Excel", "SQL", "Python",
        "Pandas", "Power BI", "Statistics",
        "Data Visualization"
    ],

    "Python Developer": [
        "Python", "OOP", "Flask",
        "SQL", "Git", "REST API",
        "File Handling"
    ],

    "Java Developer": [
        "Java", "OOP", "Collections",
        "JDBC", "Spring Boot", "SQL",
        "REST API"
    ],

    "Frontend Developer": [
        "HTML", "CSS", "JavaScript",
        "Bootstrap", "React", "Responsive Design",
        "API Integration"
    ],

    "Backend Developer": [
        "Python", "Flask", "Django",
        "SQL", "REST API", "Authentication",
        "Deployment"
    ],

    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript",
        "Flask", "SQL", "REST API",
        "Git", "Deployment"
    ],

    "Software Engineer": [
        "Data Structures", "Algorithms", "OOP",
        "Database", "Git", "Problem Solving",
        "System Design Basics"
    ],

    "Cloud Engineer": [
        "Linux", "Networking", "AWS",
        "Azure", "Docker", "CI/CD",
        "Monitoring"
    ],

    "DevOps Engineer": [
        "Linux", "Git", "Docker",
        "CI/CD", "Kubernetes", "Cloud",
        "Monitoring"
    ],

    "Cyber Security Analyst": [
        "Networking", "Linux", "Web Security",
        "OWASP", "Python", "Incident Analysis",
        "Vulnerability Assessment"
    ],

    "UI/UX Designer": [
        "Figma", "Wireframing", "Prototyping",
        "User Research", "Design Systems",
        "Usability Testing"
    ],

    "Mobile App Developer": [
        "Flutter", "React Native", "UI Design",
        "API Integration", "Firebase", "State Management"
    ],

    "QA/Test Engineer": [
        "Manual Testing", "Test Cases", "Selenium",
        "API Testing", "Bug Reporting", "Automation Testing"
    ]
}


def generate_recommendations(missing_skills):
    recommendations = []

    for skill in missing_skills:
        recommendations.append(
            f"Learn {skill} and build a small project or task using it."
        )

    if not recommendations:
        recommendations.append(
            "Great! Your current skills match this role well. Start building advanced projects."
        )

    return recommendations


@skill_gap.route("/skill-gap", methods=["GET", "POST"])
@login_required
def skill_gap_page():

    missing_skills = []
    matched_skills = []
    recommendations = []
    role = ""
    readiness_score = None

    roles = list(ROLE_SKILLS.keys())

    if request.method == "POST":

        role = request.form.get("role")

        resume_text = request.form.get(
            "resume_text",
            ""
        ).lower()

        required_skills = ROLE_SKILLS.get(role, [])

        for skill in required_skills:
            if skill.lower() in resume_text:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        if required_skills:
            readiness_score = int(
                (len(matched_skills) / len(required_skills)) * 100
            )
        else:
            readiness_score = 0

        recommendations = generate_recommendations(missing_skills)

    return render_template(
        "skill_gap.html",
        role=role,
        roles=roles,
        missing_skills=missing_skills,
        matched_skills=matched_skills,
        recommendations=recommendations,
        readiness_score=readiness_score
    )