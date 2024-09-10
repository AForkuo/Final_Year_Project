import os
from app.forms import AddCourseForm, RegistrationForm, SystemSettingsForm
from app.models.course import Course
from app.models.system_settings import SystemSetting
from app.models.user import User
from flask import Blueprint, render_template, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.security import generate_password_hash
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if current_user.role != 'admin':
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_view


@admin_bp.route('/logs')
@login_required
@admin_required
def view_logs():
    log_file = 'logs/app.log'
    if os.path.exists(log_file):
        with open(log_file, 'r') as file:
            logs = file.readlines()
    else:
        logs = ["Log file does not exist."]
    return render_template('logs.html', logs=logs, title="System Logs")

@admin_bp.route('/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, title="Add User")

@admin_bp.route('/settings', methods=['GET', 'POST'], endpoint='settings')
@login_required
@admin_required
def settings():
    form = SystemSettingsForm()

    if form.validate_on_submit():
        settings = {
            'submission_deadline': form.submission_deadline.data,
            'notification_settings': form.notification_settings.data
        }
        for key, value in settings.items():
            setting = SystemSetting.query.filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                new_setting = SystemSetting(key=key, value=value)
                db.session.add(new_setting)
        db.session.commit()
        flash('Settings have been updated', 'success')
        return redirect(url_for('admin.settings'))

    settings = {setting.key: setting.value for setting in SystemSetting.query.all()}
    form.submission_deadline.data = settings.get('submission_deadline', '')
    form.notification_settings.data = settings.get('notification_settings', '')

    return render_template('settings.html', form=form, title="System Settings")


@admin_bp.route('/delete_course/<string:course_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_course(course_id):
    form = AddCourseForm()
    course = Course.query.get_or_404(course_id)  # Get the course or show a 404 error
    
    if request.method == 'POST':
        try:
            db.session.delete(course)
            db.session.commit()
            flash(f'Course {course.name} has been deleted.', 'success')
            return redirect(url_for('admin.view_course'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting course: {e}', 'danger')
        
    return render_template('delete_course.html', course=course, form=form, title="Delete Course")

@admin_bp.route('/view_course')
@login_required
@admin_required
def view_course():
    courses = Course.query.all()
    # Add logic for assigning venues
    return render_template("view_course.html", courses=courses, title="Courses")


@admin_bp.route('/course_management')
@login_required
@admin_required
def course_management():
    # Add logic for assigning venues
    return render_template("course_management.html", title="Course Management")


@admin_bp.route('/user_management')
@login_required
@admin_required
def user_management():
    # Add logic for assigning venues
    return render_template("user_management.html", title="User Management")


@admin_bp.route('/view_users')
@login_required
@admin_required
def view_users():
    users = User.query.all()
    # Add logic for assigning venues
    return render_template("view_users.html", title="Users", users=users)


@admin_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    form = RegistrationForm()
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        
        flash(f'User {user.username} has been deleted successfully!', 'success')
        return redirect(url_for('admin.view_users'))  # Redirect to the user list or dashboard

    return render_template('delete_user.html', title="Delete User", user=user, form=form)
