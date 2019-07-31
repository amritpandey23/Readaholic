from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from book_review import bcrypt, db
from book_review.models import Admin
from book_review.admins.forms import LoginForm, AdminRegistrationForm


admins = Blueprint("admins", __name__)

# add admins
@admins.route("/admin/add", methods=["GET", "POST"])
@login_required
def add():
    form = AdminRegistrationForm()

    if form.validate_on_submit():
        admin_user = Admin(
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"),
        )
        try:
            db.session.add(admin_user)
            db.session.commit()
            flash(
                f"Successfully registered new admin with: {form.email.data}", "success"
            )
            return redirect(url_for("admins.add"))
        except:
            flash("Some error occurred", "danger")

    return render_template("add_admin.html", form=form, title="Add new admin")


# login page
@admins.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!", "success")
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            flash("Login successful", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        flash("login unsucessful", "danger")
    return render_template("login.html", form=form, title="Login as Administrator")


# logout
@admins.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

