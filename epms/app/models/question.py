from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

class Question(db.Model):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    examiner_id = Column(Integer, ForeignKey('examiner.id'), nullable=False)
    course_code = Column(String(50), ForeignKey('course.course_code'), nullable=False)
    question_text = Column(String(255), nullable=False)
    file_name = Column(String(255))
    file_path = Column(String(255))
    uploaded_at = Column(DateTime)
    status = Column(String(50))  # e.g., 'submitted', 'pending', 'approved'
    examiner = relationship('Examiner', back_populates='questions')
    course = relationship('Course', back_populates='questions')

    def __repr__(self):
        return f'<Question {self.id} for course {self.course_id}>'
