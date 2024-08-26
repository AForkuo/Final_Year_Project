# utils/notifications.py
from app import db
from app.models.notification import Notification

def send_notification(user_id, message):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()