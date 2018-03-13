from flask import Blueprint, session, redirect, render_template, url_for

from neon.auth.models import Token, db
from neon.auth.middleware import login_required


# Define blueprint
api = Blueprint("api", __name__, url_prefix="/api")