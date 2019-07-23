from book_review import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_title = db.Column(db.String(120), unique = True, nullable = False)
    author_name = db.Column(db.String(80), nullable = False)
    cover_image_file = db.Column(db.String(120), nullable = False, default = "default.jpeg")
    isbn = db.Column(db.Integer, nullable = True, default=1343)
    tiny_summary = db.Column(db.Text, nullable = False)
    review_content = db.Column(db.Text, nullable = True)
    def __repr__(self):
        return f"Title: {self.name}, Author: {self.author}, Cover Image: {self.cover_image_file}, ISBN Number: {self.isbn}"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    def __repr__(self):
        return f"Email: {self.email}"