from extensions import db


class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(256), nullable=False)
    ats_score = db.Column(db.Integer, nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref=db.backref('resumes', lazy=True))

    def __repr__(self):
        return f"<Resume {self.filename} ({self.ats_score})>"
