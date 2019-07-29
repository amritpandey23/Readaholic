from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from flask_pagedown.fields import PageDownField

# tag choices for book
book_tags = [
    ("Null", "Choose..."),
    ("education", "Education"),
    ("development", "Development"),
    ("growth", "Personal Growth"),
    ("programming", "Programming"),
    ("novel", "Novel"),
    ("fiction", "Fiction"),
]


class BookForm(FlaskForm):
    book_title = StringField(
        label="Title",
        validators=[DataRequired(), Length(max=120)],
        render_kw={"placeholder": "Perilous Shark was here"},
    )
    author_name = StringField(
        label="Author",
        validators=[DataRequired(), Length(max=40)],
        render_kw={"placeholder": "Gurton Buster"},
    )
    cover_image_file = FileField(label="Upload Cover Image")
    isbn = StringField(
        label="ISBN",
        validators=[DataRequired()],
        render_kw={"placeholder": "00991122334"},
    )
    genre = SelectField(label="Genre", choices=book_tags)
    rating = StringField(label="Rating", render_kw={"placeholder": "Out of 5 points"})
    shop_link = StringField(label="Shop Link")
    tiny_summary = TextAreaField(
        label="Tiny Summary",
        validators=[DataRequired()],
        render_kw={"placeholder": "few words ..."},
    )
    submit = SubmitField(label="Save")


class ReviewForm(FlaskForm):
    review_content = PageDownField(label="Write a review")
    submit = SubmitField(label="Save")
