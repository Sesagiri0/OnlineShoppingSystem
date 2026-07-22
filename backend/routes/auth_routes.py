from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from backend.models import user as user_model

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if user_model.get_by_email(email):
            flash("An account with that email already exists.", "error")
            return redirect(url_for("auth.register"))

        password_hash = generate_password_hash(password)
        user_model.create_user(full_name, email, password_hash, phone, address)
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = user_model.get_by_email(email)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["user_id"]
            session["user_name"] = user["full_name"]
            session["role"] = user["role"]
            flash(f"Welcome back, {user['full_name']}!", "success")
            if user["role"] == "admin":
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("product.list_products"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        new_password = request.form["new_password"]
        user = user_model.get_by_email(email)
        if not user:
            flash("No account found with that email.", "error")
            return redirect(url_for("auth.forgot_password"))
        user_model.update_password(user["user_id"], generate_password_hash(new_password))
        flash("Password updated. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html")


@auth_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = user_model.get_by_id(session["user_id"])
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        user_model.update_profile(user["user_id"], full_name, phone, address)
        session["user_name"] = full_name
        flash("Profile updated.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("profile.html", user=user)
