from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from functools import wraps
from .models import LovePage
from . import db

admin = Blueprint("admin", __name__, url_prefix="/admin")


# 🔐 LOGIN REQUIRED DECORATOR
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function


# 🔑 ADMIN LOGIN
@admin.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if (username == current_app.config["ADMIN_USERNAME"] and
            password == current_app.config["ADMIN_PASSWORD"]):

            session["admin_logged_in"] = True
            flash("Login successful ✅")
            return redirect(url_for("admin.dashboard"))

        flash("Invalid Credentials ❌")

    return render_template("admin_login.html")


# 📊 DASHBOARD
@admin.route("/dashboard")
@login_required
def dashboard():
    pages = LovePage.query.order_by(LovePage.created_at.desc()).all()
    total_pages = LovePage.query.count()
    total_views = sum(page.views for page in pages)

    return render_template(
        "admin_dashboard.html",
        pages=pages,
        total_pages=total_pages,
        total_views=total_views
    )


# ❌ DELETE PAGE
@admin.route("/delete/<string:id>")
@login_required
def delete_page(id):
    page = LovePage.query.get_or_404(id)

    db.session.delete(page)
    db.session.commit()

    flash("Page deleted successfully 🗑️")
    return redirect(url_for("admin.dashboard"))


# 🚪 LOGOUT
@admin.route("/logout")
@login_required
def logout():
    session.pop("admin_logged_in", None)
    flash("Logged out successfully 👋")
    return redirect(url_for("admin.login"))
