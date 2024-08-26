# models/course.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app import db

class Course(db.Model):
    __tablename__ = 'course'

    course_code = Column(String(50), primary_key=True)
    course_title = Column(String(255), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)

    questions = relationship('Question', back_populates='course')

