from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import required, length, email


class UserForm(FlaskForm):
    email = StringField("Email address", [required(), length(max=256), email()])
    password = PasswordField("New password")
