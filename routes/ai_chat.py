from flask import Blueprint, render_template, request
from flask_login import login_required
from google import genai
from dotenv import load_dotenv
import os
import random

load_dotenv()

ai_chat = Blueprint("ai_chat", __name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

ROLE_DATA = {
    "AI Engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "SQL", "Git", "Model Deployment"],
        "projects": {
            "beginner": ["Student Marks Prediction", "Spam Email Classifier"],
            "intermediate": ["AI Resume Analyzer", "AI Interview Bot"],
            "advanced": ["Traffic Prediction System", "Medical Image Classification"]
        }
    },
    "Machine Learning Engineer": {
        "skills": ["Python", "Scikit-learn", "Feature Engineering", "Model Evaluation", "MLOps", "SQL"],
        "projects": {
            "beginner": ["House Price Prediction", "Iris Classification"],
            "intermediate": ["Customer Churn Prediction", "Recommendation System"],
            "advanced": ["End-to-End ML Pipeline", "ML Deployment Platform"]
        }
    },
    "Data Scientist": {
        "skills": ["Python", "Statistics", "Pandas", "Machine Learning", "SQL", "Visualization"],
        "projects": {
            "beginner": ["EDA Project", "Student Performance Analysis"],
            "intermediate": ["Sales Forecasting", "Customer Segmentation"],
            "advanced": ["Fraud Detection", "Predictive Analytics Dashboard"]
        }
    },
    "Data Analyst": {
        "skills": ["Excel", "SQL", "Python", "Pandas", "Power BI", "Statistics"],
        "projects": {
            "beginner": ["Excel Sales Dashboard", "Student Data Analysis"],
            "intermediate": ["Power BI Dashboard", "Finance Data Analysis"],
            "advanced": ["Customer Churn Dashboard", "Business Analytics Case Study"]
        }
    },
    "Frontend Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "Bootstrap/Tailwind", "React", "Responsive Design", "API Integration"],
        "projects": {
            "beginner": ["Responsive Portfolio Website", "Landing Page UI"],
            "intermediate": ["Weather App using API", "Movie Search App"],
            "advanced": ["E-commerce Frontend", "Admin Dashboard with Charts"]
        }
    },
    "Backend Developer": {
        "skills": ["Python/Java", "Flask/Django/Spring Boot", "SQL", "REST APIs", "Authentication", "Deployment"],
        "projects": {
            "beginner": ["Login System", "Notes API"],
            "intermediate": ["Expense Tracker Backend", "Student Management API"],
            "advanced": ["Job Portal Backend", "Microservice API Platform"]
        }
    },
    "Full Stack Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "Flask/Django/Node.js", "SQL", "REST APIs", "Git"],
        "projects": {
            "beginner": ["Portfolio Website", "To-Do App"],
            "intermediate": ["Personal Finance Tracker", "Student Registration System"],
            "advanced": ["AI Career Copilot", "E-commerce Platform"]
        }
    },
    "Java Developer": {
        "skills": ["Java", "OOP", "Collections", "JDBC", "Spring Boot", "SQL", "REST APIs"],
        "projects": {
            "beginner": ["Bank Management System", "Library Management System"],
            "intermediate": ["Student Result Portal", "Spring Boot REST API"],
            "advanced": ["E-commerce Backend", "Job Portal using Spring Boot"]
        }
    },
    "Software Engineer": {
        "skills": ["DSA", "OOP", "Databases", "Git", "System Design Basics", "Problem Solving"],
        "projects": {
            "beginner": ["CRUD Application", "Portfolio Website"],
            "intermediate": ["Task Manager", "Online Exam System"],
            "advanced": ["Placement Platform", "Real-time Collaboration Tool"]
        }
    },
    "Cloud Engineer": {
        "skills": ["Linux", "Networking", "AWS/Azure", "Docker", "CI/CD", "Monitoring"],
        "projects": {
            "beginner": ["Static Website Hosting", "Cloud Storage Demo"],
            "intermediate": ["Deploy Flask App on Cloud", "CI/CD Pipeline"],
            "advanced": ["Cloud Monitoring Dashboard", "Auto-scaling Web App"]
        }
    },
    "DevOps Engineer": {
        "skills": ["Linux", "Git", "Docker", "CI/CD", "Kubernetes Basics", "Cloud"],
        "projects": {
            "beginner": ["Dockerize Flask App", "GitHub Actions Pipeline"],
            "intermediate": ["CI/CD for Web App", "Monitoring Setup"],
            "advanced": ["Kubernetes Deployment", "DevOps Automation Platform"]
        }
    },
    "Cyber Security Analyst": {
        "skills": ["Networking", "Linux", "Web Security", "OWASP", "Python", "Incident Analysis"],
        "projects": {
            "beginner": ["Password Strength Checker", "Port Scanner"],
            "intermediate": ["Phishing URL Detector", "Web Vulnerability Scanner"],
            "advanced": ["Security Monitoring Dashboard", "Intrusion Detection System"]
        }
    },
    "UI/UX Designer": {
        "skills": ["Figma", "Wireframing", "Prototyping", "User Research", "Design Systems"],
        "projects": {
            "beginner": ["Login Page Redesign", "Portfolio UI"],
            "intermediate": ["Mobile App Prototype", "Dashboard UI Kit"],
            "advanced": ["SaaS Product Design", "AI Career Platform UI"]
        }
    },
    "Mobile App Developer": {
        "skills": ["Flutter/React Native", "UI Design", "APIs", "Firebase", "State Management"],
        "projects": {
            "beginner": ["Calculator App", "To-Do Mobile App"],
            "intermediate": ["Expense Tracker App", "Weather App"],
            "advanced": ["Career Guidance App", "E-commerce Mobile App"]
        }
    },
    "QA/Test Engineer": {
        "skills": ["Manual Testing", "Test Cases", "Selenium", "API Testing", "Bug Reporting"],
        "projects": {
            "beginner": ["Test Cases for Login Page", "Bug Report Documentation"],
            "intermediate": ["Selenium Automation Suite", "API Testing Collection"],
            "advanced": ["Testing Framework", "QA Dashboard"]
        }
    }
}


def detect_duration(message):
    msg = message.lower()

    if "12 month" in msg or "1 year" in msg or "one year" in msg:
        return 12
    if "9 month" in msg or "nine month" in msg:
        return 9
    if "6 month" in msg or "six month" in msg or "half year" in msg:
        return 6
    if "4 month" in msg or "four month" in msg:
        return 4
    if "3 month" in msg or "three month" in msg:
        return 3
    if "2 month" in msg or "two month" in msg:
        return 2
    if "30 day" in msg or "1 month" in msg or "one month" in msg:
        return 1

    return 3


def build_dynamic_roadmap(target_role, skills, projects, duration):
    roadmap = f"Roadmap for {target_role}:\n\n"

    for month in range(1, duration + 1):
        if month == 1:
            tasks = [
                f"Learn fundamentals required for {target_role}",
                f"Start with: {', '.join(skills[:3])}",
                "Create GitHub repository and maintain daily progress",
                f"Build beginner project: {projects['beginner'][0]}"
            ]
        elif month == 2:
            tasks = [
                f"Practice intermediate skills: {', '.join(skills[3:5])}",
                "Solve practical problems and mini tasks",
                f"Build intermediate project: {projects['intermediate'][0]}",
                "Improve resume with project details"
            ]
        elif month == 3:
            tasks = [
                "Learn deployment and documentation",
                f"Build advanced project: {projects['advanced'][0]}",
                "Deploy one project online",
                "Prepare LinkedIn and GitHub profile"
            ]
        else:
            tasks = [
                "Improve existing projects with better UI and features",
                "Practice interview questions for the target role",
                "Add real-world use cases to projects",
                "Apply for internships and update resume"
            ]

        roadmap += f"Month {month}:\n"
        for task in tasks:
            roadmap += f"- {task}\n"
        roadmap += "\n"

    roadmap += "Final Advice:\n"
    roadmap += "- Do not only watch tutorials.\n"
    roadmap += "- Build, deploy, document, and explain your projects clearly.\n"
    roadmap += "- Focus on consistency and GitHub activity.\n"

    return roadmap


def role_fallback_answer(target_role, user_message):
    data = ROLE_DATA.get(target_role, ROLE_DATA["Software Engineer"])
    msg = user_message.lower()

    skills = data["skills"]
    projects = data["projects"]
    duration = detect_duration(user_message)

    if "roadmap" in msg or "plan" in msg or "learn" in msg or "month" in msg or "year" in msg:
        return build_dynamic_roadmap(
            target_role,
            skills,
            projects,
            duration
        )

    if "project" in msg or "projects" in msg:
        return f"""
Project Suggestions for {target_role}:

Beginner Projects:
- {projects["beginner"][0]}
- {projects["beginner"][1]}

Intermediate Projects:
- {projects["intermediate"][0]}
- {projects["intermediate"][1]}

Advanced Projects:
- {projects["advanced"][0]}
- {projects["advanced"][1]}

Required Skills:
{chr(10).join("- " + skill for skill in skills)}

Final Advice:
Choose one project, complete it fully, upload it to GitHub, and deploy it online.
"""

    if "skill" in msg or "skills" in msg:
        return f"""
Important Skills for {target_role}:

Technical Skills:
{chr(10).join("- " + skill for skill in skills)}

How to Practice:
- Learn one skill at a time
- Build mini tasks after each topic
- Add projects to GitHub
- Explain every project clearly in resume

Final Advice:
Do not only list skills. Prove them through working projects.
"""

    if "interview" in msg:
        return f"""
Interview Preparation for {target_role}:

Prepare These Areas:
- Core technical concepts
- Project explanation
- Resume-based questions
- Basic HR questions

Common Questions:
- Tell me about yourself.
- Explain your best project.
- What challenges did you face?
- Why do you want this role?

Final Advice:
Practice explaining projects in simple words with confidence.
"""

    return f"""
Guidance for {target_role}:

Key Skills:
{chr(10).join("- " + skill for skill in skills)}

Recommended Projects:
- {projects["beginner"][0]}
- {projects["intermediate"][0]}
- {projects["advanced"][0]}

Next Steps:
- Pick one skill to learn this week
- Build one small project
- Push it to GitHub
- Improve your resume with project details

Final Advice:
Consistency and deployed projects matter more than only certificates.
"""


@ai_chat.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    response_text = ""

    if request.method == "POST":
        user_message = request.form.get("message", "")
        expert_type = request.form.get("expert_type", "Career Mentor")
        target_role = request.form.get("target_role", "Software Engineer")
        duration = detect_duration(user_message)

        style = random.choice([
            "beginner-friendly",
            "placement-focused",
            "project-focused",
            "industry-focused",
            "interview-focused"
        ])

        prompt = f"""
You are a specialized {expert_type} for B.Tech engineering students.

Target Role:
{target_role}

Response Style:
{style}

Student Question:
{user_message}

Detected Roadmap Duration:
{duration} month(s)

Instructions:
- First understand the user question.
- Do not force the same format for every answer.
- If user asks for projects, give role-specific project ideas.
- If user asks for roadmap, give exactly {duration} month(s), not always 3 months.
- If user asks for 6 months, give Month 1 to Month 6.
- If user asks for 12 months or 1 year, give Month 1 to Month 12.
- If user asks for skills, list role-specific skills clearly.
- If user asks for interview help, give interview-specific guidance.
- Avoid generic advice.
- Keep the answer practical for an Indian B.Tech student.
- Do not claim 100% accuracy.
- Use bullet points wherever useful.
- Give a direct and useful answer.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            response_text = response.text

        except Exception:
            response_text = role_fallback_answer(
                target_role,
                user_message
            )

    return render_template(
        "chat.html",
        response=response_text
    )