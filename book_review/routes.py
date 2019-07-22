from book_review import app
from flask import render_template, url_for

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

@app.route("/book/<name>")
def book(name):
    return render_template("review.html", book_name=name)

