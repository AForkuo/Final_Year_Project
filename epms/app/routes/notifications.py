from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.notification import Notification
from app.forms import NotificationForm
from app.models.user import User

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@notifications_bp.route('/', methods=['GET'])
@login_required
def list_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    current_time = datetime.utcnow()
    return render_template('notifications/list.html', notifications=notifications, current_time=current_time, title="Notifications")

@notifications_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_notification():
    form = NotificationForm()
    if form.validate_on_submit():
        # Example: Send notification to all users (modify as needed)
        users = User.query.all()
        for user in users:
            notification = Notification(user_id=user.id, title=form.title.data, message=form.message.data)
            db.session.add(notification)
        db.session.commit()
        flash(f'Notification "{form.title.data}" sent successfully', 'success')
        return redirect(url_for('notifications.list_notifications'))
    return render_template('notifications/add.html', form=form, title="Send Notification")
