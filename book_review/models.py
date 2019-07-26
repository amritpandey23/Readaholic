from book_review import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Email: {self.email}"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(120), unique=True, nullable=False)
    title_slug = db.Column(db.String(120), unique=True, nullable=False)
    author_name = db.Column(db.String(80), nullable=False)
    cover_image_file = db.Column(db.String(120), nullable=False, default="default.jpeg")
    isbn = db.Column(db.Integer, nullable=False, default=1343)
    tiny_summary = db.Column(db.Text, nullable=False)
    review_content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Title: {self.book_title}, Author: {self.author_name}, Cover Image: {self.cover_image_file}, ISBN Number: {self.isbn}"
