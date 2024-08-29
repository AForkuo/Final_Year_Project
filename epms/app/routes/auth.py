from app.forms import ForgotPasswordForm, LoginForm, ResetPasswordForm
from app import db, mail
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
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = secrets.token_urlsafe(20)  # Generate a secure token
            user.reset_token = token
            db.session.commit()

            # Send email
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[form.email.data])
            msg.body = f'Please use the following link to reset your password: {reset_link}'
            mail.send(msg)

            flash('A password reset link has been sent to your email address.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('No account with that email address.', 'danger')

    return render_template('forgot_password.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if user is None:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password.data)
        user.reset_token = None  # Clear the token
        db.session.commit()

        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form)