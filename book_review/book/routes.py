from slugify import slugify
from markdown2 import Markdown
from flask import Blueprint, flash, render_template, redirect, url_for, abort, request
from flask_login import login_required
from book_review import db
from book_review.models import Book
from book_review.book.forms import BookForm, ReviewForm
from book_review.book.utils import save_cover_image, delete_cover_image

markdowner = Markdown()

book = Blueprint("book", __name__)

# add book
@book.route("/book/add", methods=["GET", "POST"])
@login_required
def add():
    form = BookForm()

    if form.validate_on_submit():
        filename = save_cover_image(form.cover_image_file)
        book = Book(
            book_title=form.book_title.data,
            title_slug=slugify(form.book_title.data),
            author_name=form.author_name.data,
            cover_image_file=filename if filename else "default.jpeg",
            isbn=form.isbn.data,
            genre=form.genre.data,
            tiny_summary=form.tiny_summary.data,
        )
        try:
            db.session.add(book)
            db.session.commit()
        except:
            flash("Something went wrong while adding book to the database.", "danger")
            return render_template("add_book.html", form=form)

        flash("Book successfully added to the database", "success")
        return redirect(url_for("main.home"))

    return render_template("add_book.html", form=form, title="Add Book")


# book page
@book.route("/book/<book_slug>")
def present(book_slug):
    book = Book.query.filter_by(title_slug=book_slug).first()
    return render_template("book.html", book=book, title=book.book_title, markdowner=markdowner)


@book.route("/book/genre/<name>")
def genre(name):
    return redirect(url_for("main.home"))


# edit book page
@book.route("/book/<book_slug>/edit", methods=["GET", "POST"])
@login_required
def edit(book_slug):
    book = Book.query.filter_by(title_slug=book_slug).first()

    if not book:
        abort(403)

    form = BookForm()

    if form.validate_on_submit():
        book.book_title = form.book_title.data
        book.author_name = form.author_name.data
        book.isbn = form.isbn.data
        book.tiny_summary = form.tiny_summary.data
        if form.cover_image_file.data:
            book.cover_image_file = form.cover_image_file.data
        try:
            db.session.commit()
        except:
            flash("Something went wrong while adding book to the database.", "danger")
            return render_template(
                "add_book.html", title=f"Edit {book.book_title}", form=form
            )
        flash("The book was updated!", "success")
        return redirect(url_for("book.present", book_slug=book.title_slug))
    elif request.method == "GET":
        form.book_title.data = book.book_title
        form.author_name.data = book.author_name
        form.isbn.data = book.isbn
        form.tiny_summary.data = book.tiny_summary

    return render_template(
        "add_book.html", title=f"Edit {book.book_title}", form=form, book=book
    )


# delete book
@book.route("/book/<book_slug>/delete", methods=["POST"])
@login_required
def delete(book_slug):
    book = Book.query.filter_by(title_slug=book_slug).first()

    if not book:
        abort(403)
    try:
        db.session.delete(book)
        db.session.commit()
        if book.cover_image_file != "default.jpg":
            delete_cover_image(book.cover_image_file)
    except:
        flash(f"Something went wrong!", "danger")
        return redirect(url_for("book.edit", book_slug=book_slug))
    flash(f"Alright, {book.book_title} was successfully deleted", "success")
    return redirect(url_for("main.home"))


# review page
@book.route("/book/<book_slug>/write_review", methods=["GET", "POST"])
@login_required
def write_review(book_slug):
    form = ReviewForm()
    book = Book.query.filter_by(title_slug=book_slug).first()
    if form.validate_on_submit():
        if form.save_draft.data:
            try:
                book.review_content = form.review_content.data
                db.session.commit()
            except:
                flash("Something went wrong")
        elif form.publish.data:
            if not form.review_content.data:
                flash("Cannot publish empty review!", "danger")
                return redirect(url_for("book.write_review", book_slug=book.title_slug))
            try:
                book.review_content = form.review_content.data
                book.review_finish = True
                db.session.commit()
            except:
                flash("Something went wrong")
            return redirect(url_for("book.present", book_slug=book.title_slug))
    elif request.method == "GET":
        form.review_content.data = book.review_content
    return render_template("write_review.html", form=form, title="Write Review")

