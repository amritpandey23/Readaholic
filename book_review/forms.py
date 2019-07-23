from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, message="Password must be 6 characters long")])
    submit = SubmitField("Login")

class ReviewForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired(), Length(max=120)])
    author = StringField(label="Author", validators=[DataRequired(), Length(max=40)])
    cover_image = StringField(label="Cover Image", default="default.jpeg", validators=[DataRequired()])
    short_description = TextAreaField(label="Short description of the book", validators=[DataRequired()])
    isbn = StringField(label="ISBN Number", default="1234", validators=[DataRequired()])
    review_text = TextAreaField(label="Write Review", validators=[DataRequired()])
    submit = SubmitField(label="Add Review")