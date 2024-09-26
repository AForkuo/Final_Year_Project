# routes/main.py
from datetime import datetime
from functools import wraps
from operator import and_
from app.models.schedule import Schedule
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import app
from app.forms import AddCourseForm, RegistrationForm, ScheduleForm, UploadQuestionForm
from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, jsonify
from flask_login import login_required, current_user
from app.models import User, Question, Course, Notification
from app.utils.notifications import send_notification
from app import db


main_bp = Blueprint('main', __name__)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    total_uploaded_questions = Question.query.count()
    total_approved_questions = Question.query.filter_by(confirm_status='Confirmed').count()
    total_pending_questions = Question.query.filter_by(confirm_status='unconfirmed').count()
    printed_questions = Question.query.filter_by(print_status='printed').count()
    pending_printing_questions = Question.query.filter_by(print_status='pending').count()
    total_courses = Course.query.count()
    total_users = User.query.count()
    chief_examiners = User.query.filter_by(role='chief_examination_officer').count()
    examiners = User.query.filter_by(role='examiner').count()
    printing_agents = User.query.filter_by(role='printing_agent').count()
    admins = User.query.filter_by(role='admin').count()
    my_uploads = Question.query.filter_by(examiner_id=current_user.user_id).count()
    my_questions_confirmed = Question.query.filter(
        and_(
            Question.examiner_id == current_user.user_id,
            Question.confirm_status == 'Confirmed'
        )
).count()
    my_questions_printed = Question.query.filter(
        and_(
            Question.examiner_id == current_user.user_id,
            Question.print_status == 'printed'
        )
).count()


    # New course-related statistics
    courses_with_questions = Course.query.join(Question).distinct().count()
    courses_without_questions = total_courses - courses_with_questions

    data = {}
    if current_user.role == 'chief_examination_officer':
        data['courses'] = Course.query.all()
    elif current_user.role == 'admin':
        data['users'] = User.query.all()

    # Pass the new course data to the template
    return render_template('dashboard.html',
                            data=data,
                            total_uploaded_questions=total_uploaded_questions,
                            total_approved_questions=total_approved_questions,
                            total_pending_questions=total_pending_questions,
                            printed_questions=printed_questions,
                            pending_printing_questions=pending_printing_questions,
                            total_courses=total_courses,
                            total_users=total_users,
                            chief_examiners=chief_examiners,
                            examiners=examiners,
                            printing_agents=printing_agents,
                            admins=admins,
                            courses_with_questions=courses_with_questions,
                            courses_without_questions=courses_without_questions,
                            my_uploads=my_uploads,
                            my_questions_confirmed=my_questions_confirmed,
                            my_questions_printed=my_questions_printed,
                            title="Dashboard")






@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = RegistrationForm()
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

    return render_template('profile.html', user=current_user, form=form, title="Profile")

@main_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = RegistrationForm()
    if request.method == 'POST':
        user = User.query.get(current_user.user_id)
        try:
            if not check_password_hash(user.password, request.form.get('current_password')):
                flash('Incorrect old password. Please try again.', 'danger')
                return redirect(url_for('main.change_password'))
        
            user.password = generate_password_hash(request.form.get('new_password'))
            db.session.commit()

            flash('Your password has been changed.', 'success')
            return redirect(url_for('main.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
            return redirect(url_for('main.profile'))

    return render_template('profile.html', user=current_user, form=form, title="Profile")


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




@main_bp.route('/assign_invigilators')
@login_required
def assign_invigilators():
    # Add logic for assigning invigilators
    return "Assign Invigilators Page"


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

@main_bp.route('/schedule')
@login_required
def view_schedule():
    # Get filter values from request.args
    exam_date = request.args.get('exam_date')
    course_code = request.args.get('course_code')
    examiner_id = request.args.get('examiner')

    # Build query based on filters
    query = Schedule.query

    if exam_date:
        query = query.filter(Schedule.exam_date == exam_date)
    if course_code:
        query = query.filter(Schedule.course_code == course_code)
    if examiner_id:
        query = query.filter(Schedule.examiner_id == examiner_id)

    schedules = query.all()
    
    courses = Course.query.all()  # Assuming you have a Course model
    examiners = User.query.filter_by(role='examiner').all()  # Assuming examiners have a 'role' attribute

    return render_template('schedule.html', schedules=schedules, courses=courses, examiners=examiners, title="Exam Schedule")


@main_bp.route('/schedule/add', methods=['GET', 'POST'])
@login_required
def add_schedule():
    form = ScheduleForm()
    form.course_code.choices = [(course.course_code, course.course_code) for course in Course.query.all()]
    form.examiner_id.choices = [(examiner.user_id, examiner.username) for examiner in User.query.filter_by(role='examiner').all()]

    if form.validate_on_submit():
        new_schedule = Schedule(
            exam_date=form.exam_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            venue=form.venue.data,
            course_code=form.course_code.data,
            examiner_id=form.examiner_id.data
        )
        db.session.add(new_schedule)
        db.session.commit()
        flash('Schedule added successfully!', 'success')
        return redirect(url_for('main.view_schedule'))

    return render_template('add_edit_schedule.html', form=form, title="Add Schedule")

@main_bp.route('/schedule/edit/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
def edit_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    form = ScheduleForm(obj=schedule)
    form.course_code.choices = [(course.course_code, course.course_code) for course in Course.query.all()]
    form.examiner_id.choices = [(examiner.id, examiner.name) for examiner in User.query.filter_by(role='examiner').all()]

    if form.validate_on_submit():
        schedule.exam_date = form.exam_date.data
        schedule.start_time = form.start_time.data
        schedule.end_time = form.end_time.data
        schedule.venue = form.venue.data
        schedule.course_code = form.course_code.data
        schedule.examiner_id = form.examiner_id.data
        db.session.commit()
        flash('Schedule updated successfully!', 'success')
        return redirect(url_for('main.view_schedule'))

    return render_template('add_edit_schedule.html', form=form, title="Edit Schedule")