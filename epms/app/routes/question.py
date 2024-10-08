from datetime import datetime
import os
import uuid
import app
from app.models.course import Course
from flask import Blueprint, render_template, redirect, jsonify, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.forms import ApproveQuestionForm, UploadQuestionForm
from app.models.question import Question
from app.forms import PrintForm
from app.utils.print_utils import print_file

question_bp = Blueprint('question', __name__, url_prefix='/questions')



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@question_bp.route('/upload_questions', methods=['GET', 'POST'])
@login_required
def upload_questions():
    form = UploadQuestionForm()
    if request.method == "POST":
        file = request.files.get('question_file')  # Safely get the file
         
        if not file:
            flash('No file part', 'danger')
            return redirect(request.url)

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file_name = str(uuid.uuid1()) + "_" + filename

        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
        file.save(file_path)

        new_question = Question(
            course_code=form.course.data,
            file_name=file_name,
            file_path=file_path,
            uploaded_at=datetime.utcnow(),
            examiner_id=current_user.user_id
        )

        db.session.add(new_question)
        db.session.commit()

        flash('File successfully uploaded', 'success')
        return redirect(url_for('question.my_uploads'))

    return render_template('questions/upload_questions.html', form=form, title="File Upload")

    

@question_bp.route('/my_questions')
@login_required
def my_questions():
    questions = Question.query.filter_by(examiner_id=current_user.id).all()
    return render_template('my_questions.html', questions=questions)


@question_bp.route('/view_file/<filename>')
@login_required
def view_file(filename):
    # Ensure the filename is secure
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)



@question_bp.route('/print_questions', methods=['GET', 'POST'])
@login_required
def print_questions():
    form = PrintForm()
    confirmed_questions = Question.query.filter_by(confirm_status='Confirmed').all()
    return render_template('print_questions.html', form=form, questions=confirmed_questions, title="Print Questions")

@question_bp.route('/print_selected_questions', methods=['POST'])
@login_required
def print_selected_questions():
    selected_question_ids = request.form.getlist('question_ids')
    if selected_question_ids:
        questions_to_print = Question.query.filter(Question.id.in_(selected_question_ids)).all()
        for question in questions_to_print:
            if question.file_path and os.path.exists(question.file_path):
                print_file(question.file_path)  # Print the file
                question.status = 'Printed'
            else:
                flash(f'File for question {question.id} not found or path is invalid.', 'warning')
        db.session.commit()
        flash(f'{len(questions_to_print)} questions marked as printed.', 'success')
    else:
        flash('No questions selected.', 'warning')
    return redirect(url_for('question.print_questions'))


@question_bp.route('/approve_questions', methods=['GET', 'POST'])
@login_required
def approve_questions():
    # Query all questions
    form = ApproveQuestionForm()
    questions = Question.query.all()
    
    if request.method == 'POST':
        question_ids = request.form.getlist('question_ids')  # Get selected question IDs
        
        # Update the approved status of selected questions
        if question_ids:
            for q_id in question_ids:
                question = Question.query.get(int(q_id))
                if question:
                    question.confirm_status = "Confirmed"
            db.session.commit()
            flash('Selected questions have been approved!', 'success')
        else:
            flash('No questions selected for approval.', 'danger')
        
        return redirect(url_for('question.approve_questions'))
    
    return render_template('questions/approve_questions.html', questions=questions, form=form, title="Approve Questions")


@question_bp.route('/my_uploads', methods=['GET', 'POST'])
@login_required
def my_uploads():
    # Query all questions
    questions = Question.query.filter_by(examiner_id=current_user.user_id).all()
    
    return render_template('questions/my_uploads.html', questions=questions, title="My Uploads")
