from slugify import slugify
from markdown2 import Markdown
from flask import Blueprint, flash, render_template, redirect, url_for, abort, request
from flask_login import login_required
from book_review import db
from book_review.models import Book, Comment
from book_review.book.forms import BookForm, ReviewForm, CommentForm
from book_review.book.utils import save_cover_image, delete_cover_image

markdowner = Markdown()

book = Blueprint("book", __name__)

# book/comment page
@book.route("/book/<book_slug>", methods=["GET", "POST"])
def present(book_slug):
    book = Book.query.filter_by(title_slug=book_slug).first()
    comments = Comment.query.filter_by(book_id=book.id).order_by(Comment.date_added.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        for comment in comments:
            if comment.email == form.email.data and comment.book_id == book.id:
                flash(f"Cannot post this comment as you've already posted once.", "info")
                return redirect(url_for("book.present", book_slug=book.title_slug))
        comment = Comment(
            name=form.name.data,
            email=form.email.data,
            comment_text=form.comment_text.data,
            book_id=book.id,
        )
        try:
            db.session.add(comment)
            db.session.commit()
            flash("Comment was posted successfully!", "success")
            return redirect(url_for("book.present", book_slug=book.title_slug))
        except:
            flash("something went wrong!", "danger")

    return render_template(
        "book.html",
        book=book,
        title=book.book_title,
        markdowner=markdowner,
        form=form,
        comments=comments,
    )


# add book
@book.route("/book/add", methods=["GET", "POST"])
@login_required
def add():
    form = BookForm()

    if form.validate_on_submit():

        saved_book = Book.query.filter_by(isbn = form.isbn.data).first()
        if saved_book:
            flash(f"{saved_book.book_title} already exist in database!", "danger")
        else:
            filename = save_cover_image(form.cover_image_file)
            book = Book(
                book_title=form.book_title.data,
                title_slug=slugify(form.book_title.data),
                author_name=form.author_name.data,
                cover_image_file=filename if filename else "default.jpeg",
                isbn=form.isbn.data,
                genre=form.genre.data,
                tiny_summary=form.tiny_summary.data,
                rating=form.rating.data,
                shop_link = form.shop_link.data
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
        book.shop_link = form.shop_link.data
        book.rating = form.rating.data
        book.tiny_summary = form.tiny_summary.data
        book.genre = form.genre.data
        if form.cover_image_file.data:
            delete_cover_image(book.cover_image_file)
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
        form.genre.data = book.genre
        form.shop_link.data = book.shop_link
        form.rating.data = book.rating

    return render_template(
        "add_book.html", title=f"Edit {book.book_title}", form=form, book=book
    )


# delete book
@book.route("/book/<book_slug>/delete", methods=["POST"])
@login_required
def delete(book_slug):
    book = Book.query.filter_by(title_slug=book_slug).first()
    comments = Comment.query.filter_by(book_id=book.id).all()
    if not book:
        abort(403)
    try:
        for comment in comments:
            db.session.delete(comment)
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
                book.review_content_draft = form.review_content.data
                db.session.commit()
                flash("Draft was saved successfully", "success")
            except:
                flash("Something went wrong", "danger")
        elif form.publish.data:
            if not form.review_content.data:
                flash("Cannot publish empty review!", "danger")
                return redirect(url_for("book.write_review", book_slug=book.title_slug))
            try:
                book.review_content = form.review_content.data
                book.review_content_draft = form.review_content.data
                db.session.commit()
                flash("Review was published.", "success")
            except:
                flash("Something went wrong", "danger")
            return redirect(url_for("book.present", book_slug=book.title_slug))
    elif request.method == "GET":
        form.review_content.data = book.review_content_draft
    return render_template("write_review.html", form=form, book=book, title="Write Review")


@book.route("/books/search")
def search():
    search_query = request.args.get("bname", type=str)
    if not search_query:
        abort(404)
    books = Book.query.filter(Book.book_title.contains(search_query)).all()
    return render_template("list_books.html", title=f"Search results for \"{search_query}\"", books=books)

# book filtered by genre
@book.route("/books/genre/<name>")
def genre(name):
    books = Book.query.filter_by(genre = name).all()
    return render_template("list_books.html", books=books, title=f"Books on {name}")
