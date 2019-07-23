from book_review import db

class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    author = db.Column(db.String(80), nullable = False)
    cover_image = db.Column(db.String(120), nullable = False, default = "default.jpeg")
    short_description = db.Column(db.Text, nullable = False)
    isbn = db.Column(db.Integer, nullable = True, default=1343)
    review_text = db.Column(db.Text, nullable = False)
    def __repr__(self):
        return f"Name: {self.name}, Author: {self.author}"

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(100), nullable = False)