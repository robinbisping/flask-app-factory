from flask import Blueprint, session, redirect, render_template, url_for
from datetime import datetime

from .models import db, User
from .forms import LoginForm, RegistrationForm


# Define blueprint
auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Registers a user"""
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user object
        user = User(form.email.data, form.password.data)
        user.last_login = datetime.now()
        # Insert user into the database
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
        # Create session
        session["user_id"] = user.id
        # Redirect to the admin area
        return redirect(url_for("admin.index"))
    return render_template("auth/registration.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Logs a user in"""
    form = LoginForm()
    if form.validate_on_submit():
        # Load user from database
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists and password is correct
        if user and user.verify_password(form.password.data):
            user.last_login = datetime.now()
            try:
                db.session.commit()
            except Exception as e:
                print(e)
            # Create session
            session["user_id"] = user.id
            # Redirect to the admin area
            return redirect(url_for("admin.index"))
    return render_template("auth/login.html", form=form)


@auth.route("/logout", methods=["GET"])
def logout():
    """Logs a user out"""
    # Delete session
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
