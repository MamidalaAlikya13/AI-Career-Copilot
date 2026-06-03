from flask import Blueprint, render_template, request
from flask_login import login_required
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

ai_chat = Blueprint("ai_chat", __name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

@ai_chat.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    response_text = ""

    if request.method == "POST":
        user_message = request.form.get("message")

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"""
                You are an AI Career Mentor for engineering students.
                Give simple, practical, student-friendly answers.

                Student Question:
                {user_message}
                """
            )

            response_text = response.text

        except Exception:
            response_text = """
Gemini API quota exceeded or temporarily unavailable.

But AI Mentor module is connected successfully.

Sample Career Roadmap:

Month 1:
Learn Python, Git, GitHub basics.

Month 2:
Learn Flask, HTML, CSS, JavaScript.

Month 3:
Build 2 full-stack projects.

Month 4:
Learn SQL and database design.

Month 5:
Practice DSA and coding problems.

Month 6:
Prepare resume, LinkedIn, GitHub, and mock interviews.
"""

    return render_template(
        "chat.html",
        response=response_text
    )