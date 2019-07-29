from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_pagedown.fields import PageDownField
from book_review.models import Admin


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(
        label="Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Password should be 6 characters long"),
        ],
    )
    submit = SubmitField(label="Login")


class AdminRegistrationForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        label="Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register this user as admin")

    # check if user is already registered in database
    def validate_email(self, email):
        admin_user = Admin.query.filter_by(email=email.data).first()
        if admin_user:
            raise ValidationError(
                f"{admin_user.email} is already registered.", "warning"
            )

