import os
from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_required
from routes.ai_chat import ai_chat as ai_chat_bp
from extensions import db, login_manager
from routes.analytics import analytics as analytics_bp
from models.user import User
from routes.auth import auth as auth_bp
from routes.resume import resume as resume_bp
from routes.roadmap import roadmap as roadmap_bp
from routes.mock_interview import mock_interview as mock_interview_bp
from routes.project_recommender import project_recommender as project_recommender_bp
from routes.portfolio import portfolio as portfolio_bp
from routes.skill_gap import skill_gap as skill_gap_bp
from routes.about import about as about_bp


def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY',
        'dev-secret-key'
    )

    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'site.db')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(mock_interview_bp)
    app.register_blueprint(ai_chat_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(project_recommender_bp)
    app.register_blueprint(portfolio_bp)
    app.register_blueprint(skill_gap_bp)
    app.register_blueprint(about_bp)

    # User Loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create Database Tables
    with app.app_context():
        db.create_all()

    # Routes
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        return redirect(url_for('auth.login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template(
            'dashboard.html',
            user=current_user
        )

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)