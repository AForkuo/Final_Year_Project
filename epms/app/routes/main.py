# routes/main.py
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import app
from app.forms import AddCourseForm, UploadQuestionForm
from app.models.examiner import Examiner
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from app.models import User, Question, Course, Schedule, Venue, InvigilatorAssignment, Notification
from app.utils.notifications import send_notification
from app import db


main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    data = {}
    if current_user.role == 'chief_examination_officer':
        data['pending_questions'] = Question.query.filter_by(status='pending').all()
        data['courses'] = Course.query.all()
    elif current_user.role == 'examiner':
        data['my_questions'] = Question.query.filter_by(examiner_id=current_user.id).all()
    elif current_user.role == 'admin':
        data['users'] = User.query.all()
    elif current_user.role == 'printing_agent':
        data['approved_questions'] = Question.query.filter_by(status='approved').all()
    elif current_user.role == 'chief_invigilator':
        data['venues'] = Venue.query.all()
        data['assignments'] = InvigilatorAssignment.query.all()
    return render_template('dashboard.html', data=data, title="Dashboard")


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            current_user.username = request.form.get('username')
            current_user.email = request.form.get('email')
            # Update other fields as necessary
            db.session.commit()
            flash('Your profile has been updated.', 'success')
            return redirect(url_for('main.profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
            return redirect(url_for('main.profile'))

    return render_template('profile.html', user=current_user, title="Profile")


@main_bp.route('/set_submission_date', methods=['GET', 'POST'])
@login_required
def set_submission_date():
    if request.method == 'POST':
        course_id = request.form['course_id']
        submission_date = request.form['submission_date']
        course = Course.query.get(course_id)
        if course:
            for question in course.questions:
                question.submission_date = submission_date
                examiner = User.query.get(question.examiner_id)
                if examiner:
                    send_notification(examiner.id, f'Submission date for course {course.name} is set to {submission_date}.')
            db.session.commit()
        return redirect(url_for('main.view_courses'))
    courses = Course.query.all()
    return render_template('set_submission_date.html', courses=courses)



@main_bp.route('/courses')
@login_required
def view_courses():
    courses = Course.query.all()
    return render_template('view_courses.html', courses=courses, title="Courses")



@main_bp.route('/print_questions')
@login_required
def print_questions():
    questions = Question.query.all()
    if request.method == 'POST':
        selected_questions = request.form.getlist('selected_questions')
        if selected_questions:
            # Logic for printing the questions
            flash(f"Printing {len(selected_questions)} question(s).")
            # Update question status to 'printed' if necessary
            for question_id in selected_questions:
                question = Question.query.get(question_id)
                question.status = 'printed'
                db.session.commit()
            return redirect(url_for('print_questions'))
    return render_template('print_questions.html', questions=questions, title='Print Question')

@main_bp.route('/assign_invigilators')
@login_required
def assign_invigilators():
    # Add logic for assigning invigilators
    return "Assign Invigilators Page"

@main_bp.route('/approve_questions')
@login_required
def approve_questions():
    # Add logic for approving questions
    return "Approve Questions Page"

@main_bp.route('/set_deadlines')
@login_required
def set_deadlines():
    # Add logic for setting submission deadlines
    return "Set Submission Deadlines Page"


@main_bp.route('/submission_status')
def view_submission_status():
    # Query to get all examiners and their submission status
    examiners = db.session.query(Examiner).all()
    submission_status = []
    
    for examiner in examiners:
        total_courses = db.session.query(Course).count()
        submitted_questions = db.session.query(Question).filter_by(examiner_id=examiner.id, status='submitted').count()
        pending_courses = total_courses - submitted_questions

        submission_status.append({
            'examiner': examiner,
            'submitted': submitted_questions,
            'pending': pending_courses
        })

    return render_template('submission_status.html', submission_status=submission_status)

@main_bp.route('/edit_questions')
@login_required
def edit_questions():
    # Add logic for editing submitted questions
    return "Edit Questions Page"


@main_bp.route('/track_print_jobs')
@login_required
def track_print_jobs():
    # Add logic for tracking print jobs
    return "Track Print Jobs Page"

@main_bp.route('/assign_venues')
@login_required
def assign_venues():
    # Add logic for assigning venues
    return "Assign Venues Page"

@main_bp.route('/monitor_exams')
@login_required
def monitor_exams():
    # Add logic for monitoring exams
    return "Monitor Exams Page"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.role == 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/add_course', methods=['GET', 'POST'])
@admin_required
def add_course():
    form = AddCourseForm()
    if form.validate_on_submit():
        course = Course(course_title=form.name.data, course_code=form.code.data, credit_hours=form.credit_hours.data)
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('main.view_courses'))
    return render_template('add_course.html', form=form, title="Add Course")


@main_bp.route('/examination_planning')
@login_required
def examination_planning():
    # Add logic for assigning venues
    return render_template("examination_planning.html", title="Examination Planning")


@main_bp.route('/questions_management')
@login_required
def questions_management():
    # Add logic for assigning venues
    return render_template("questions_management.html", title="Manage Questions")


@main_bp.route('/printing_and_dist')
@login_required
def printing_and_dist():
    # Add logic for assigning venues
    return render_template("printing_and_dist.html", title="Printing and Distribution")


