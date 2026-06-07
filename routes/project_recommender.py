from flask import Blueprint, render_template, request
from flask_login import login_required
from google import genai
from dotenv import load_dotenv
import os
import random

load_dotenv()

project_recommender = Blueprint("project_recommender", __name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

PROJECTS = {
    "AI Engineer": {
        "Beginner": [
            "Student Marks Prediction",
            "Spam Email Classifier",
            "Simple Chatbot",
            "Image Classifier",
            "Sentiment Analysis App",
            "Handwritten Digit Classifier",
            "AI Study Planner",
            "Basic Recommendation System"
        ],
        "Intermediate": [
            "AI Resume Analyzer",
            "AI Interview Preparation Bot",
            "Fake News Detection System",
            "Traffic Prediction Dashboard",
            "AI Career Roadmap Generator",
            "Smart Attendance System",
            "Emotion Detection App",
            "AI Notes Summarizer"
        ],
        "Advanced": [
            "AI-Powered Traffic Management System",
            "Medical Image Diagnosis System",
            "AI Career Copilot Platform",
            "Smart Surveillance Detection System",
            "Multi-Agent Interview Evaluator",
            "AI Hiring Assistant",
            "Personalized Learning Recommendation System",
            "AI Research Paper Summarizer"
        ]
    },

    "Machine Learning Engineer": {
        "Beginner": [
            "House Price Prediction",
            "Iris Flower Classification",
            "Loan Approval Prediction",
            "Movie Recommendation Basics",
            "Car Price Prediction",
            "Diabetes Prediction",
            "Email Spam Classifier",
            "Student Performance Predictor"
        ],
        "Intermediate": [
            "Customer Churn Prediction",
            "Recommendation System",
            "Credit Card Fraud Detection",
            "Stock Price Trend Predictor",
            "Employee Attrition Prediction",
            "Sales Forecasting Model",
            "Text Classification System",
            "Product Recommendation Engine"
        ],
        "Advanced": [
            "End-to-End ML Pipeline",
            "ML Model Deployment Platform",
            "MLOps Monitoring Dashboard",
            "Real-time Prediction API",
            "Automated ML Training Platform",
            "Model Drift Detection System",
            "Feature Store Prototype",
            "Scalable ML Inference Service"
        ]
    },

    "Data Scientist": {
        "Beginner": [
            "Exploratory Data Analysis Project",
            "Student Performance Analysis",
            "Titanic Survival Analysis",
            "Weather Data Analysis",
            "Netflix Dataset Analysis",
            "IPL Data Analysis",
            "Healthcare Data Analysis",
            "E-commerce Data Exploration"
        ],
        "Intermediate": [
            "Sales Forecasting System",
            "Customer Segmentation",
            "Fraud Detection Model",
            "HR Attrition Prediction",
            "Market Basket Analysis",
            "Loan Risk Prediction",
            "Customer Lifetime Value Prediction",
            "Social Media Sentiment Analysis"
        ],
        "Advanced": [
            "Predictive Analytics Dashboard",
            "Business Intelligence ML Platform",
            "Risk Analysis System",
            "Real-time Analytics Platform",
            "AI-based Business Decision System",
            "Financial Risk Prediction Platform",
            "Healthcare Prediction Dashboard",
            "End-to-End Data Science Case Study"
        ]
    },

    "Data Analyst": {
        "Beginner": [
            "Excel Sales Dashboard",
            "Student Data Analysis",
            "COVID Data Visualization",
            "Expense Analysis Dashboard",
            "Retail Sales Analysis",
            "Survey Data Analysis",
            "College Placement Analysis",
            "Simple KPI Dashboard"
        ],
        "Intermediate": [
            "Power BI Business Dashboard",
            "Customer Churn Dashboard",
            "Finance Data Dashboard",
            "E-commerce Sales Analysis",
            "HR Analytics Dashboard",
            "Marketing Campaign Analysis",
            "SQL Business Reports",
            "Product Sales Dashboard"
        ],
        "Advanced": [
            "End-to-End Business Analytics Case Study",
            "Real-time KPI Dashboard",
            "Executive Analytics Dashboard",
            "Market Basket Analysis Dashboard",
            "Customer Insights Platform",
            "Operations Analytics Dashboard",
            "Financial Performance Dashboard",
            "Multi-source Analytics Dashboard"
        ]
    },

    "Frontend Developer": {
        "Beginner": [
            "Responsive Portfolio Website",
            "Landing Page UI",
            "Product Card Design",
            "Login/Register Page UI",
            "Restaurant Website",
            "Photography Portfolio",
            "Pricing Table UI",
            "Animated Profile Card"
        ],
        "Intermediate": [
            "Weather App using API",
            "Movie Search App",
            "Quiz Application",
            "Expense Tracker Frontend",
            "Recipe Finder App",
            "GitHub Profile Finder",
            "Interactive Dashboard UI",
            "To-Do App with Local Storage"
        ],
        "Advanced": [
            "E-commerce Frontend",
            "Admin Dashboard with Charts",
            "Job Portal Frontend",
            "AI Career Copilot Frontend UI",
            "Learning Platform Frontend",
            "Real-time Chat UI",
            "SaaS Landing Page System",
            "Portfolio Builder Frontend"
        ]
    },

    "Backend Developer": {
        "Beginner": [
            "Login System Backend",
            "Notes API",
            "Student CRUD API",
            "Simple Blog Backend",
            "Contact Form Backend",
            "Basic REST API",
            "User Profile API",
            "Task API"
        ],
        "Intermediate": [
            "Expense Tracker Backend",
            "Student Management API",
            "Authentication API",
            "File Upload System",
            "Role-based Login System",
            "Blog API with Comments",
            "Payment Record API",
            "API with Pagination"
        ],
        "Advanced": [
            "Job Portal Backend",
            "Microservice-based API Platform",
            "Role-based Access Control System",
            "Scalable REST API System",
            "Notification Backend",
            "Analytics API Platform",
            "Secure File Management System",
            "Multi-user SaaS Backend"
        ]
    },

    "Full Stack Developer": {
        "Beginner": [
            "Portfolio Website",
            "To-Do App with Database",
            "Student Registration System",
            "Blog Application",
            "Contact Manager",
            "Notes App",
            "Simple Feedback App",
            "Basic Event Registration App"
        ],
        "Intermediate": [
            "Personal Finance Tracker",
            "Student Placement Portal",
            "Online Course Platform",
            "Task Management Web App",
            "Resume Analyzer",
            "Inventory Management System",
            "Appointment Booking App",
            "Mini CRM System"
        ],
        "Advanced": [
            "AI Career Copilot",
            "E-commerce Platform",
            "Learning Management System",
            "Freelance Marketplace Platform",
            "Job Portal Platform",
            "AI Interview Platform",
            "Project Collaboration Tool",
            "SaaS Analytics Dashboard"
        ]
    },

    "Python Developer": {
        "Beginner": [
            "Expense Tracker",
            "Quiz Application",
            "File Organizer",
            "Library Management System",
            "Password Generator",
            "Calculator App",
            "Text Formatter",
            "Contact Book"
        ],
        "Intermediate": [
            "Flask CRUD App",
            "PDF Resume Analyzer",
            "API-based Weather App",
            "Automation Script Collection",
            "Email Automation Tool",
            "Web Scraper",
            "Data Cleaning Tool",
            "Image Processing App"
        ],
        "Advanced": [
            "AI Resume Screening System",
            "Web Scraping Dashboard",
            "Python Automation Platform",
            "Flask SaaS Application",
            "AI Chatbot Platform",
            "PDF Report Generator",
            "Workflow Automation System",
            "Data Pipeline Tool"
        ]
    },

    "Java Developer": {
        "Beginner": [
            "Bank Management System",
            "Library Management System",
            "Student Record System",
            "Console Billing System",
            "ATM Simulation",
            "Employee Record System",
            "Quiz App",
            "Contact Management System"
        ],
        "Intermediate": [
            "Student Result Portal",
            "Spring Boot REST API",
            "Inventory Management System",
            "Employee Management System",
            "Online Voting System",
            "Hospital Management System",
            "Course Registration System",
            "Ticket Booking System"
        ],
        "Advanced": [
            "E-commerce Backend",
            "Job Portal using Spring Boot",
            "Online Banking System",
            "Microservices with Spring Boot",
            "Learning Management Backend",
            "Enterprise CRM Backend",
            "Payment Management System",
            "Cloud-ready Java API"
        ]
    },

    "Software Engineer": {
        "Beginner": [
            "CRUD Application",
            "Portfolio Website",
            "Calculator App",
            "Notes Manager",
            "Simple File Manager",
            "Basic Chat App",
            "Task Tracker",
            "Student Portal"
        ],
        "Intermediate": [
            "Task Manager",
            "Online Exam System",
            "Bug Tracking System",
            "Code Snippet Manager",
            "Versioned Notes App",
            "Team Collaboration Board",
            "API-based Dashboard",
            "College Management System"
        ],
        "Advanced": [
            "Placement Preparation Platform",
            "Real-time Collaboration Tool",
            "Scalable Project Management App",
            "System Design Simulator",
            "Distributed Task Queue",
            "Multi-role SaaS Platform",
            "Real-time Notification System",
            "Developer Productivity Dashboard"
        ]
    }
}


def get_fallback_projects(role, level):
    role_projects = PROJECTS.get(role, PROJECTS["Software Engineer"])

    if level == "Mixed":
        all_projects = []
        for projects in role_projects.values():
            all_projects.extend(projects)

        return random.sample(all_projects, min(5, len(all_projects)))

    projects = role_projects.get(level, role_projects["Beginner"])
    return random.sample(projects, min(5, len(projects)))


def parse_ai_projects(text):
    projects = []

    for line in text.splitlines():
        clean = line.strip()

        if not clean:
            continue

        clean = clean.lstrip("-•*0123456789. )")

        if len(clean) > 5:
            projects.append(clean)

    return projects[:5]


@project_recommender.route("/project-recommender", methods=["GET", "POST"])
@login_required
def recommender():
    selected_goal = ""
    selected_level = ""
    recommendations = []
    roles = list(PROJECTS.keys())
    levels = ["Beginner", "Intermediate", "Advanced", "Mixed"]

    if request.method == "POST":
        selected_goal = request.form.get("goal")
        selected_level = request.form.get("level")

        prompt = f"""
You are a technical project mentor for B.Tech students.

Generate 5 unique, original, resume-worthy project ideas.

Target Role:
{selected_goal}

Project Level:
{selected_level}

Rules:
- Do not repeat common generic ideas if possible.
- Make projects practical for college students.
- Each project should be different from the others.
- Keep each idea as one clear line.
- Do not add long explanation.
- Do not use numbering if possible.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            recommendations = parse_ai_projects(response.text)

            if len(recommendations) < 3:
                recommendations = get_fallback_projects(
                    selected_goal,
                    selected_level
                )

        except Exception:
            recommendations = get_fallback_projects(
                selected_goal,
                selected_level
            )

    return render_template(
        "project_recommender.html",
        selected_goal=selected_goal,
        selected_level=selected_level,
        recommendations=recommendations,
        roles=roles,
        levels=levels
    )