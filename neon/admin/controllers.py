from flask import Blueprint, session, redirect, render_template, url_for

from neon.auth.models import Token, db
from neon.auth.middleware import login_required

from .forms import UserForm


# Define blueprint
admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/", methods=["GET"])
@login_required
def index(user):
    return redirect(url_for("admin.edit_account"))


@admin.route("/account/edit", methods=["GET", "POST"])
@login_required
def edit_account(user):
    form = UserForm()
    if form.validate_on_submit():
        # Store new information in the user object
        user.email = form.email.data
        if form.password.data:
            user.password = form.password.data
        # Insert changes into the database
        try:
            db.session.commit()
        except Exception as e:
            print(e)
    return render_template("admin/account.html", form=form, user=user)


@admin.route("/account/tokens", methods=["GET"])
@login_required
def tokens(user):
    # Load all tokens of the current user from the database
    tokens = Token.query.filter_by(user_id=user.id).all()
    return render_template("admin/tokens.html", user=user, tokens=tokens)


@admin.route("/account/token/add", methods=["GET"])
@login_required
def add_token(user):
    # Create a new token object
    token = Token(user.id)
    # Insert token into the database
    db.session.add(token)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
    return redirect(url_for("admin.tokens"))


@admin.route("/account/token/delete/<int:token_id>", methods=["GET"])
@login_required
def delete_token(user, token_id):
    # Load token object from database
    token = Token.query.filter_by(id=token_id).first()
    # Check if token exists and is owned by the current user
    if token and token.user_id == user.id:
        # Delete token from database
        db.session.delete(token)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
    return redirect(url_for("admin.tokens"))
