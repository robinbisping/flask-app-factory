from functools import wraps
from flask import abort, redirect, request, session, url_for

from .models import User


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get user id from session cookie
        user_id = session.get("user_id")
        if user_id:
            # Find user in database
            user = User.query.filter_by(id=user_id).first()
            # If user exists, call wrapped function (with user as first argument)
            if user:
                return f(user, *args, **kwargs)
        # Redirect to the login page if the user is not logged in
        return redirect(url_for("auth.login"))
    return wrapper


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Get authorization header
        auth = request.authorization
        if auth:
            # Find user in database
            user = User.query.filter_by(email=auth.username).first()
            # If user exists and password is correct, call wrapped function
            if user and user.verify_password(auth.password):
                return f(*args, **kwargs)
        # Abort if authorization failed
        abort(403)
    return wrapper
