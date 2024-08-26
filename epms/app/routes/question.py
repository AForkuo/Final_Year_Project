from datetime import datetime
import os
import app
from app.models.course import Course
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.forms import UploadQuestionForm
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
    if form.validate_on_submit():
        file = form.question_file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully', 'success')
            return "file uploaded success"
        else:
            flash('Invalid file type', 'error')

    return render_template('questions/upload.html', form=form)

# def upload_question():
#     form = UploadQuestionForm()
#     # if request.method == "POST":
#     #     uploaded_file = request.files['file']
#     #     if uploaded_file.filename != '':
#     #         uploaded_file.save(uploaded_file.filename)
        
#     if form.validate_on_submit():

#         # new_question = Question(
#         #         examiner_id=current_user.id,  # Ensure this matches your model's field
#         #         question_text=form.question_text.data,
                
                
#         #         uploaded_at=datetime.utcnow(),
#         #         status='pending',
#         #         course_code=form.course.data
                
#         #     )
#         file = form.question_file.data

#         # if file is None:
#         #     flash('No file part', 'danger')
#         #     return redirect(request.url)

#         # if file.filename == '':
#         #     flash('No selected file', 'danger')
#         #     return redirect(request.url)

#         filename = secure_filename(file.filename)
#         # new_question.file_name=filename
#         form.fileName.file.save(os.path.join(app.Config['UPLOAD_FOLDER'], filename))
       
#         # new_question.file_path=file_path

            
#         # path_list = new_question.file_path.split('/')[1:]
#         # new_path = '/'.join(path_list)

#         # Save file info to the database

#         # new_question.file_path = new_path
#         # db.session.add(new_question)
#         # db.session.commit()

#         # flash('File successfully uploaded', 'success')
#         return redirect(url_for('question.upload_question'))

#     return render_template('questions/upload.html', form=form, title="File Upload")
    
    


@question_bp.route('/my_questions')
@login_required
def my_questions():
    questions = Question.query.filter_by(examiner_id=current_user.id).all()
    return render_template('my_questions.html', questions=questions)

# @question_bp.route('/uploads/<filename>')
# @login_required
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




@question_bp.route('/print_questions', methods=['GET', 'POST'])
@login_required
def print_questions():
    form = PrintForm()
    questions = Question.query.all()
    return render_template('print_questions.html', form=form, questions=questions)

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
    return redirect(url_for('questions.print_questions'))
