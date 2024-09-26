from app.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField, DateTimeField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
from app.models.course import Course

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
        ('chief_examination_officer', 'Chief Examination Officer'),
        ('examiner', 'Examiner'),
        ('admin', 'Admin'),
        ('printing_agent', 'Printing Agent'),
        ('chief_invigilator', 'Chief Invigilator')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Log in as:', choices=[
        ('chief_examination_officer', 'Chief Examination Officer'),
        ('examiner', 'Examiner'),
        ('admin', 'Admin'),
        ('printing_agent', 'Printing Agent')
    ], validators=[DataRequired()])
    submit = SubmitField('Login')


class SystemSettingsForm(FlaskForm):
    submission_deadline = StringField('Submission Deadline', validators=[DataRequired()])
    notification_settings = StringField('Notification Settings', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class NotificationForm(FlaskForm):
    title = TextAreaField('Title', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Notification')


class UploadQuestionForm(FlaskForm):
    course = SelectField('Course', coerce=str, validators=[DataRequired()])
    question_file = FileField('Question File', validators=[
        FileRequired(),
        FileAllowed(['pdf', '.doc', 'docx', 'txt'], 'Only document, and text files are allowed!')
    ])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    submit = SubmitField('Upload')

    def __init__(self, *args, **kwargs):
        super(UploadQuestionForm, self).__init__(*args, **kwargs)
        self.course.choices = [(course.course_code, course.course_title) for course in Course.query.all()]

   
class ApproveQuestionForm(FlaskForm):
    submit = SubmitField('Approve')


class AddCourseForm(FlaskForm):
    name = StringField('Course Title', validators=[DataRequired(), Length(max=100)])
    code = StringField('Course Code', validators=[DataRequired(), Length(max=20)])
    credit_hours = IntegerField('Credit Hours', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add Course')


class ScheduleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    start = DateTimeField('Start', validators=[DataRequired()])
    end = DateTimeField('End', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    examiner = SelectField('Examiner', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.examiner.choices = [(examiner.id, examiner.username) for examiner in User.query.filter_by(role='examiner').all()]


class PrintForm(FlaskForm):
    submit = SubmitField('Print')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class ScheduleForm(FlaskForm):
    exam_date = DateField('Exam Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    course_code = SelectField('Course Code', validators=[DataRequired()], choices=[])  # Populate dynamically
    examiner_id = SelectField('Examiner', validators=[DataRequired()], choices=[])  # Populate dynamically
    submit = SubmitField('Save')

