from book_review import app, db
from flask import render_template, url_for, flash, redirect, request
from book_review.forms import LoginForm, ReviewForm
from book_review.models import Admin, Books

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

@app.route("/")
@app.route("/catalog")
def home():
    return render_template("home.html", books=books)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email = form.email.data).first()
        if admin and admin.password == form.password.data:
            flash("Login successful", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        flash("login unsucessful", "danger")
    return render_template("login.html", form=form)

@app.route("/book/<name>")
def book(name):
    return render_template("review.html", book_name=name)

@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    form = ReviewForm()
    if form.validate_on_submit():
        book = Books(
            name = form.name.data,
            author = form.author.data,
            cover_image = form.cover_image.data,
            short_description = form.short_description.data,
            isbn = form.isbn.data,
            review_text = form.review_text.data
        )
        db.session.add(book)
        db.session.commit()
        flash("book successfully added to the database", "success")
        return redirect(url_for("home"))

    return render_template("add_review.html", form=form)