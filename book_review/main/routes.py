import os
from flask import Blueprint, render_template, request, send_from_directory
from book_review import app
from book_review.models import Book

main = Blueprint("main", __name__)


# home page
@main.route("/", methods=["GET"])
def home():
    page = request.args.get("page", default=1, type=int)
    books = Book.query.paginate(page=page, per_page=8)
    return render_template("home.html", books=books, title="Home", curr_page=page)


# about page
@main.route("/about", methods=["GET"])
def about():
    return render_template("about.html", title="About")


# send image file
@main.route("/uploads/<filename>")
def send_image_file(filename):
    return send_from_directory(os.path.join(app.instance_path, "uploads"), filename)
