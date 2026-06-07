from flask import Blueprint, render_template, request, flash
from flask_login import login_required

roadmap = Blueprint("roadmap", __name__)

ROLE_DATA = {
    "AI Engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "SQL", "Git", "Model Deployment"],
        "projects": ["AI Resume Analyzer", "AI Interview Bot", "Traffic Prediction System"]
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "Scikit-learn", "Feature Engineering", "Model Evaluation", "MLOps", "SQL"],
        "projects": ["House Price Prediction", "Customer Churn Prediction", "End-to-End ML Pipeline"]
    },
    "Data Scientist": {
        "skills": ["Python", "Statistics", "Pandas", "Machine Learning", "SQL", "Data Visualization"],
        "projects": ["EDA Project", "Sales Forecasting", "Fraud Detection System"]
    },
    "Data Analyst": {
        "skills": ["Excel", "SQL", "Python", "Pandas", "Power BI", "Statistics"],
        "projects": ["Excel Dashboard", "Power BI Dashboard", "Customer Churn Analysis"]
    },
    "Python Developer": {
        "skills": ["Python", "OOP", "Flask", "SQL", "Git", "REST API"],
        "projects": ["CLI Expense Tracker", "Flask CRUD App", "API-based Web App"]
    },
    "Java Developer": {
        "skills": ["Java", "OOP", "Collections", "JDBC", "Spring Boot", "SQL"],
        "projects": ["Bank Management System", "Student Result Portal", "Spring Boot REST API"]
    },
    "Frontend Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "Bootstrap/Tailwind", "React", "Responsive Design"],
        "projects": ["Portfolio Website", "Weather App using API", "E-commerce Frontend"]
    },
    "Backend Developer": {
        "skills": ["Python/Java", "Flask/Django/Spring Boot", "SQL", "REST API", "Authentication"],
        "projects": ["Login System", "Student Management API", "Job Portal Backend"]
    },
    "Full Stack Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "Flask/Django/Node.js", "SQL", "REST API"],
        "projects": ["Student Registration System", "Personal Finance Tracker", "AI Career Copilot"]
    },
    "Software Engineer": {
        "skills": ["DSA", "OOP", "Databases", "Git", "Problem Solving", "System Design Basics"],
        "projects": ["Task Manager", "Online Exam System", "Placement Preparation Platform"]
    },
    "Cloud Engineer": {
        "skills": ["Linux", "Networking", "AWS/Azure", "Docker", "CI/CD", "Monitoring"],
        "projects": ["Static Website Hosting", "Deploy Flask App on Cloud", "Cloud Monitoring Dashboard"]
    },
    "DevOps Engineer": {
        "skills": ["Linux", "Git", "Docker", "CI/CD", "Kubernetes Basics", "Cloud"],
        "projects": ["Dockerize Flask App", "GitHub Actions Pipeline", "Kubernetes Deployment"]
    },
    "Cyber Security Analyst": {
        "skills": ["Networking", "Linux", "Web Security", "OWASP", "Python", "Incident Analysis"],
        "projects": ["Password Strength Checker", "Phishing URL Detector", "Security Monitoring Dashboard"]
    },
    "UI/UX Designer": {
        "skills": ["Figma", "Wireframing", "Prototyping", "User Research", "Design Systems"],
        "projects": ["Login Page Redesign", "Mobile App Prototype", "SaaS Product Design"]
    },
    "Mobile App Developer": {
        "skills": ["Flutter/React Native", "UI Design", "API Integration", "Firebase", "State Management"],
        "projects": ["To-Do Mobile App", "Weather App", "Career Guidance App"]
    },
    "QA/Test Engineer": {
        "skills": ["Manual Testing", "Test Cases", "Selenium", "API Testing", "Bug Reporting"],
        "projects": ["Test Cases for Login Page", "Selenium Automation Suite", "QA Dashboard"]
    }
}


INTERVIEW_TIPS = [
    "Prepare a strong self-introduction.",
    "Practice explaining every project clearly.",
    "Revise core technical concepts for your target role.",
    "Prepare resume-based questions.",
    "Do mock interviews and improve communication."
]


def parse_skills(raw_skills):
    skills = []

    for segment in raw_skills.split(","):
        name = segment.strip()

        if name:
            skills.append(name)

    return skills


def get_duration_units(duration):
    if duration == "30 Days":
        return 4, "Week"
    if duration == "3 Months":
        return 3, "Month"
    if duration == "6 Months":
        return 6, "Month"
    if duration == "12 Months":
        return 12, "Month"

    return 4, "Week"


def generate_period_plan(role, role_skills, projects, duration):
    count, unit = get_duration_units(duration)

    plan = []

    for index in range(1, count + 1):
        if unit == "Week":
            if index == 1:
                focus = "Understand fundamentals and setup learning environment."
                actions = [
                    f"Learn basics required for {role}.",
                    f"Start with: {', '.join(role_skills[:3])}.",
                    "Create GitHub repository for practice.",
                    f"Start beginner project: {projects[0]}."
                ]
            elif index == 2:
                focus = "Practice tools and build small tasks."
                actions = [
                    f"Practice: {', '.join(role_skills[2:5])}.",
                    "Build small tasks instead of only watching tutorials.",
                    "Document progress in README files.",
                    f"Continue project: {projects[0]}."
                ]
            elif index == 3:
                focus = "Strengthen missing skills and project quality."
                actions = [
                    "Improve weak areas from skill gap analysis.",
                    f"Start intermediate project: {projects[1]}.",
                    "Add clean UI, validation, or real-world data.",
                    "Push all changes to GitHub."
                ]
            else:
                focus = "Interview and portfolio preparation."
                actions = [
                    "Prepare project explanation.",
                    "Update resume and LinkedIn.",
                    "Practice mock interviews.",
                    "Deploy one project online."
                ]
        else:
            if index == 1:
                focus = "Foundation building."
                actions = [
                    f"Learn fundamentals of {role}.",
                    f"Focus on: {', '.join(role_skills[:3])}.",
                    "Set up GitHub and learning tracker.",
                    f"Build beginner project: {projects[0]}."
                ]
            elif index == 2:
                focus = "Core skill development."
                actions = [
                    f"Practice: {', '.join(role_skills[3:6])}.",
                    "Build mini projects after each topic.",
                    f"Improve beginner project: {projects[0]}.",
                    "Start documenting your work."
                ]
            elif index == 3:
                focus = "Intermediate project building."
                actions = [
                    f"Build intermediate project: {projects[1]}.",
                    "Add authentication, API, dashboard, or analytics where relevant.",
                    "Push clean code to GitHub.",
                    "Improve README with screenshots."
                ]
            elif index == 4:
                focus = "Advanced role-specific learning."
                actions = [
                    "Learn advanced tools related to the role.",
                    f"Start advanced project: {projects[2]}.",
                    "Add deployment and documentation.",
                    "Practice role-specific interview questions."
                ]
            elif index == 5:
                focus = "Portfolio and resume strengthening."
                actions = [
                    "Polish UI and project structure.",
                    "Add live demo links to resume.",
                    "Create LinkedIn project post.",
                    "Do mock interviews."
                ]
            elif index == 6:
                focus = "Internship and placement preparation."
                actions = [
                    "Apply for internships.",
                    "Revise DSA/core subjects.",
                    "Practice HR and technical questions.",
                    "Finalize GitHub and portfolio."
                ]
            else:
                focus = "Advanced growth and specialization."
                actions = [
                    "Deepen role-specific expertise.",
                    "Build or upgrade one advanced project.",
                    "Contribute to open source or collaborate with peers.",
                    "Apply consistently for internships and roles."
                ]

        plan.append({
            "period": f"{unit} {index}",
            "focus": focus,
            "actions": actions
        })

    return plan


def generate_roadmap(role, skills, duration):
    data = ROLE_DATA.get(role, ROLE_DATA["Software Engineer"])

    target_skills = data["skills"]
    projects = data["projects"]

    current_skills = {
        skill.strip().lower()
        for skill in skills
    }

    found_skills = [
        skill
        for skill in target_skills
        if skill.lower() in current_skills
    ]

    missing_skills = [
        skill
        for skill in target_skills
        if skill.lower() not in current_skills
    ]

    plan = generate_period_plan(
        role,
        target_skills,
        projects,
        duration
    )

    return {
        "goal": role,
        "duration": duration,
        "current_skills": skills,
        "missing_skills": missing_skills,
        "found_skills": found_skills,
        "recommended_projects": projects,
        "interview_tips": INTERVIEW_TIPS,
        "plan": plan,
    }


@roadmap.route("/roadmap", methods=["GET", "POST"])
@login_required
def roadmap_view():
    roles = list(ROLE_DATA.keys())
    durations = ["30 Days", "3 Months", "6 Months", "12 Months"]

    if request.method == "POST":
        career_goal = request.form.get("career_goal", "").strip()
        duration = request.form.get("duration", "30 Days")
        current_skills = parse_skills(
            request.form.get("current_skills", "")
        )

        if not career_goal:
            flash("Please select a career goal.", "danger")
            return render_template(
                "roadmap.html",
                roles=roles,
                durations=durations
            )

        roadmap_data = generate_roadmap(
            career_goal,
            current_skills,
            duration
        )

        return render_template(
            "roadmap.html",
            roadmap=roadmap_data,
            roles=roles,
            durations=durations,
            selected_role=career_goal,
            selected_duration=duration
        )

    return render_template(
        "roadmap.html",
        roles=roles,
        durations=durations
    )