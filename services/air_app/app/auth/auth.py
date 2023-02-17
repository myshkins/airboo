"""authentication routes"""
from flask import Blueprint, render_template

auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)


@auth_bp.route("/auth", endpoint="auth", methods=["GET", "POST"])
def login():
    """render login view, authenticate user if valid and login user"""
    return render_template("login.html")
