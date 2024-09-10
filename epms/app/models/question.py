from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(50), db.ForeignKey('course.course_code', ondelete='CASCADE'), nullable=False)
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime)
    print_status = db.Column(db.String(20), nullable=False, default='pending')
    confirm_status = db.Column(db.String(20), nullable=False, default='unconfirmed')
    examiner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    course = db.relationship('Course', back_populates='questions')
    examiner = db.relationship('User', backref=db.backref('questions', lazy=True))

    def __repr__(self):
        return f'<Question {self.id} for course {self.course_code}>'
