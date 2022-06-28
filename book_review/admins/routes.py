from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from book_review import bcrypt, db
from book_review.models import Admin, Comment, Book
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

@admins.route("/comments")
@login_required
def comments():
    com = Comment.query.join(Book, Book.id == Comment.book_id)\
    .add_columns(
        Book.book_title, 
        Comment.id,
        Comment.comment_text, 
        Comment.date_added, 
        Comment.email, 
        Comment.name,
        Comment.verified)\
    .order_by(Comment.date_added.desc())\
    .all()
    return render_template("comments.html", comments=com)

@admins.route("/comment/approve/<comment_id>")
def approve_comment(comment_id):
    com = Comment.query.filter_by(id=comment_id).first()
    if not com:
        flash("Comment id not found", "info")
        redirect(url_for('admins.comments'))
    try:
        com.verified = True
        db.session.commit()
    except:
        flash("Some error occured in the database", "danger")
        return redirect(url_for("admins.comments"))
    flash("Comment was successfully approved", "success")
    return redirect(url_for("admins.comments"))
    
@admins.route("/comment/delete/<comment_id>")
def delete_comment(comment_id):
    com = Comment.query.filter_by(id=comment_id).first()
    if not com:
        flash("Comment id not found", "info")
        redirect(url_for("admins.comments"))
    try:
        db.session.delete(com)
        db.session.commit()
    except:
        flash("Some error occured in the database", "danger")
        return redirect(url_for("admins.comments"))
    flash("Comment was successfully removed", "success")
    return redirect(url_for("admins.comments"))
