from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), ForeignKey('course.course_code'), nullable=False)
    question_text = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime)
    status = db.Column(db.String(50))  # e.g., 'submitted', 'pending', 'approved'
    is_approved = db.Column(db.Boolean, default=False)
    course = db.relationship('Course', back_populates='questions')

    def __repr__(self):
        return f'<Question {self.id} for course {self.course_id}>'
