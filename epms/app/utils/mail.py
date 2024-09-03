from flask import url_for, current_app
from flask_mail import Message
from app import mail 


def send_reset_email(user):
    """Sends an email with a token to reset the user's password."""
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@example.com',
                  recipients=[user.email])
    
    reset_link = url_for('auth.reset_password', token=token, _external=True)
    msg.body = f'''To reset your password, visit the following link:
{reset_link}

If you did not make this request, simply ignore this email and no changes will be made.
'''

    mail.send(msg)
