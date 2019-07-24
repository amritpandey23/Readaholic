from book_review import app, db
from flask import render_template, url_for, flash, redirect, request
from book_review.forms import LoginForm, ReviewForm
from book_review.models import Admin, Book
from flask_login import login_user, logout_user, current_user, login_required

from slugify import slugify

books = [
    {
        "name": "Cracking the Coding Interview",
        "description": "Some quick example text to build on the card title and make up the bulk of the card's content.",
        "slug": "cracking-the-coding-interview"
    },
    {
        "name": "The C Programming Language",
        "description": "Some quick example text to build on the card title and make up the bulk of the card's content.",
        "slug": "the-c-programming-language"
    }
]

# home page
@app.route("/")
@app.route("/catalog")
def home():
    return render_template("home.html", books=books)

# about page
@app.route("/about")
def about():
    return render_template("about.html", title="About")

# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in!", "success")
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email = form.email.data).first()
        if admin and admin.password == form.password.data:
            login_user(admin)
            flash("Login successful", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        flash("login unsucessful", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# add reviews page
@app.route("/add_review", methods=["GET", "POST"])
@login_required
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        f = form.cover_image_file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            '/Users/amrit/Desktop/Projects/Review-Book-Site/static/img', filename
        ))
        book = Book(
            book_title = form.book_title.data,
            title_slug = slugify(form.book_title.data),
            author_name = form.author_name.data,
            cover_image_file = form.cover_image_file.data,
            isbn = form.isbn.data,
            tiny_summary = form.tiny_summary.data,
            review_content = form.review_content.data
        )
        try:
            db.session.add(book)
            db.session.commit()
        except:
            flash("Failed! Something went wrong while commiting book to the database.", "danger")
            return render_template("add_review.html", form=form)
            
        flash("book successfully added to the database", "success")
        return redirect(url_for("home"))

    return render_template("add_review.html", form=form)

@app.route("/add_admin", methods=["GET", "POST"])
@login_required
def add_admin():
    form = AdminForm()
    if form.validate_on_submit():
        admin_user = Admin(
            email = form.email.data,
            password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        )
        try:
            db.session.add(admin_user)
            db.session.commit()
            flash(f"Successfully registered new admin with: {form.email.data}", "success")
        except:
            flash("Some error occurred", "danger")
        
    
    return render_template("add_admin.html", form = form, title = "Add new admin")

# book page
@app.route("/book/<name>")
def book(name):
    return render_template("review.html", book_name=name)