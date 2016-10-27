from flask import render_template
from flask_mail import Message

from todo_app.extensions.mail import mail

DEFAULT_SENDER = 'Team Todo <help@todo.com>'


def send_reset_password(user, password):
    msg = Message("Reset Your Password",
                  sender=DEFAULT_SENDER,
                  recipients=[user.email])

    msg.html = render_template('emails/reset_password.html', user=user, password=password)

    mail.send(msg)
