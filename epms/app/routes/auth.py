from app.forms import ForgotPasswordForm, LoginForm, RequestResetForm, ResetPasswordForm
from app import db, bcrypt
from app.utils.mail import send_reset_email
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash,  generate_password_hash
from app.models.user import User
import secrets
from flask_mail import Message

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = form.role.data
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if user.role == role:  # Validate the role
                login_user(user)
                flash('Login successful', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid role selected', 'danger')
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Add more routes like register, if necessary


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('That is an invalid or expired token', 'warning')
        try:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        except Exception as e:
            flash('Could not send email. Please try again later.', 'danger')
            print(e)

        return redirect(url_for('auth.login'))
    
    return render_template('forgot_password.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Route to reset the password using a token."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)



