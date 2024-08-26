# models/examiner.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app import db

class Examiner(db.Model):
    __tablename__ = 'examiner'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    questions = relationship('Question', back_populates='examiner')
