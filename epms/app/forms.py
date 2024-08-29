from app.models.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
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
    question_text = TextAreaField('Question Text', validators=[Optional()])
    question_file = FileField('Question File', validators=[
        FileRequired(),
        FileAllowed(['pdf', '.doc', 'docx', 'txt'], 'Only document, and text files are allowed!')
    ])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    submit = SubmitField('Upload')

    def __init__(self, *args, **kwargs):
        super(UploadQuestionForm, self).__init__(*args, **kwargs)
        self.course.choices = [(course.course_code, course.course_title) for course in Course.query.all()]

   


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