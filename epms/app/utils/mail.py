# utils/mail.py
from flask_mail import Message
from app import mail

def send_notification(subject, recipient, body):
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)
