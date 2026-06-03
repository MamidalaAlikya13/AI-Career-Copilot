from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user

roadmap = Blueprint('roadmap', __name__)

BASE_SKILLS = {
    'data scientist': ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Data Visualization'],
    'web developer': ['HTML', 'CSS', 'JavaScript', 'REST API', 'Flask'],
    'backend developer': ['Python', 'SQL', 'Flask', 'REST API', 'Git'],
    'frontend developer': ['HTML', 'CSS', 'JavaScript', 'REST API', 'Git'],
    'machine learning engineer': ['Python', 'Machine Learning', 'SQL', 'Git', 'REST API'],
}

COMMON_PROJECTS = {
    'data scientist': [
        'Build a predictive model using Python and real-world data.',
        'Create a data visualization dashboard for insights.',
    ],
    'web developer': [
        'Build a responsive website with HTML, CSS, and JavaScript.',
        'Create a Flask app with REST API endpoints.',
    ],
    'backend developer': [
        'Build an API service using Flask and SQL database.',
        'Add authentication and unit tests to your backend project.',
    ],
    'frontend developer': [
        'Create a dynamic SPA using HTML, CSS, JavaScript.',
        'Build a portfolio website demonstrating responsive design.',
    ],
    'machine learning engineer': [
        'Train and deploy a machine learning model with Python.',
        'Build a ML pipeline including data preprocessing and evaluation.',
    ],
}

DEFAULT_PROJECTS = [
    'Create a portfolio project that demonstrates your target role skills.',
    'Document a project on GitHub with README, instructions, and outcomes.',
]

INTERVIEW_TIPS = [
    'Practice explaining your projects and the technologies you used.',
    'Review core concepts and interview questions for your target role.',
    'Prepare a short elevator pitch describing your experience and goals.',
    'Practice with mock interviews and feedback from peers.',
]

SKILL_KEYWORDS = [
    'Python', 'SQL', 'Flask', 'Git', 'Machine Learning',
    'REST API', 'HTML', 'CSS', 'JavaScript', 'Data Visualization', 'Statistics'
]


def parse_skills(raw_skills):
    skills = []
    for segment in raw_skills.split(','):
        name = segment.strip()
        if name:
            skills.append(name)
    return skills


def infer_goal_category(goal_text):
    if not goal_text:
        return None

    normalized = goal_text.lower()
    if 'data' in normalized and 'scientist' in normalized:
        return 'data scientist'
    if 'machine' in normalized:
        return 'machine learning engineer'
    if 'backend' in normalized or 'api' in normalized:
        return 'backend developer'
    if 'frontend' in normalized or 'web' in normalized:
        return 'web developer'
    return None


def generate_roadmap(goal, skills):
    category = infer_goal_category(goal)
    current_skills = {skill.title() for skill in skills}
    if category and category in BASE_SKILLS:
        target_skills = BASE_SKILLS[category]
    else:
        target_skills = SKILL_KEYWORDS

    missing_skills = [skill for skill in target_skills if skill not in current_skills]
    found_skills = [skill for skill in target_skills if skill in current_skills]

    if category and category in COMMON_PROJECTS:
        recommended_projects = COMMON_PROJECTS[category] + DEFAULT_PROJECTS
    else:
        recommended_projects = DEFAULT_PROJECTS

    thirty_day_plan = [
        {
            'week': 'Week 1',
            'focus': 'Clarify goals, learn fundamentals, and build a study plan.',
            'actions': [
                'Review your career goal and identify key skills.',
                'Refresh fundamentals in Python, HTML/CSS, or SQL as needed.',
                'Start a small project or tutorial related to your target role.',
            ],
        },
        {
            'week': 'Week 2',
            'focus': 'Build practical experience and practice tools.',
            'actions': [
                'Work on one or two focused projects.',
                'Learn version control with Git and publish code to GitHub.',
                'Study REST APIs, frameworks, or machine learning basics.',
            ],
        },
        {
            'week': 'Week 3',
            'focus': 'Strengthen missing skills and polish projects.',
            'actions': [
                'Fill gaps in the missing skill list.',
                'Add features and documentation to your projects.',
                'Practice solving role-specific problems and coding exercises.',
            ],
        },
        {
            'week': 'Week 4',
            'focus': 'Prepare for interviews and finalize your portfolio.',
            'actions': [
                'Review common interview questions and practice answers.',
                'Update your resume and portfolio with recent projects.',
                'Do mock interviews and identify areas to improve.',
            ],
        },
    ]

    return {
        'goal': goal,
        'current_skills': sorted(current_skills),
        'missing_skills': missing_skills,
        'found_skills': found_skills,
        'recommended_projects': recommended_projects,
        'interview_tips': INTERVIEW_TIPS,
        'thirty_day_plan': thirty_day_plan,
    }


@roadmap.route('/roadmap', methods=['GET', 'POST'])
@login_required
def roadmap_view():
    if request.method == 'POST':
        career_goal = request.form.get('career_goal', '').strip()
        current_skills = parse_skills(request.form.get('current_skills', ''))

        if not career_goal:
            flash('Please enter a career goal.', 'danger')
            return render_template('roadmap.html')

        roadmap_data = generate_roadmap(career_goal, current_skills)
        return render_template('roadmap.html', roadmap=roadmap_data)

    return render_template('roadmap.html')
