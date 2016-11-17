from flask import render_template
from flask_mail import Message

from app.extensions.mail_ext import mail

DEFAULT_SENDER = 'Team Todo <help@example.com>'


def send_reset_password(user, password):
    msg = Message("Reset Your Password", sender=DEFAULT_SENDER, recipients=[user.email])
    msg.html = render_template('emails/reset_password.html', user=user, password=password)
    mail.send(msg)
