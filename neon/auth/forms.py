from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import required, length, email


class LoginForm(FlaskForm):
    email = StringField("Email address", [required()])
    password = PasswordField("Password", [required()])


class RegistrationForm(FlaskForm):
    email = StringField("Email address", [required(), length(max=256), email()])
    password = PasswordField("Password", [required()])
