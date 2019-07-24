from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from book_review.models import Admin

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email(), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, message="Password should be 6 characters long")])
    submit = SubmitField("Login")

class ReviewForm(FlaskForm):
    book_title = StringField(label="Title", validators=[DataRequired(), Length(max=120)])
    author_name = StringField(label="Author", validators=[DataRequired(), Length(max=40)])
    cover_image_file = FileField(label="Upload Cover Image")
    isbn = StringField(label="ISBN", default="1234", validators=[DataRequired()])
    tag = SelectField(label="Tag", choices=[("edu", "Education"), ("dev", "Development")])
    tiny_summary = TextAreaField(label="Tiny Summary", validators=[DataRequired()])
    review_content = TextAreaField(label="Review", validators=[DataRequired()])
    submit = SubmitField(label="Add Review")

class AdminForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register this user as admin")

    def validate_email(self, email):
        admin_user = Admin.query.filter_by(email = email.data).first()
        if admin_user:
            raise ValidationError("That email is already registered.", "warning")