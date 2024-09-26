from app import db

class SecurityQuestion(db.Model):
    __tablename__ = 'security_question'

    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)  # Store hashed answers if using bcrypt
