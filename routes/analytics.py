from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.resume import Resume
from models.interview import Interview

analytics = Blueprint("analytics", __name__)

@analytics.route("/analytics")
@login_required
def analytics_page():
    resumes = Resume.query.filter_by(user_id=current_user.id).all()
    interviews = Interview.query.filter_by(user_id=current_user.id).all()

    latest_resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.id.desc()).first()

    latest_ats = latest_resume.ats_score if latest_resume else 0
    total_interviews = len(interviews)

    if total_interviews > 0:
        avg_score = round(sum(i.score for i in interviews) / total_interviews, 1)
    else:
        avg_score = 0

    readiness = int((latest_ats * 0.6) + (avg_score * 10 * 0.4))

    badges = []

    if resumes:
        badges.append("🏅 First Resume Uploaded")
    if latest_ats >= 70:
        badges.append("🏆 Strong Resume Score")
    if interviews:
        badges.append("🎤 First Mock Interview Completed")
    if avg_score >= 8:
        badges.append("🔥 Interview Ready")

    return render_template(
        "analytics.html",
        latest_ats=latest_ats,
        total_interviews=total_interviews,
        avg_score=avg_score,
        readiness=readiness,
        badges=badges,
        interviews=interviews
    )