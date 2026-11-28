# CELL 13 - FLASK FORMS

from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    InputRequired,
    Email,
    Length
)


class RegisterForm(FlaskForm):

    email = StringField(
        "Email",
        description="Your school email address",
        default="student@tup.edu.ph",
        validators=[
            InputRequired(),
            Email(),
            Length(max=50)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(min=4, max=128)
        ]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired()
        ]
    )

    submit = SubmitField("Login")


# Additional Exercise 2

from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):

    display_name = StringField(
        "Display Name",
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    profile_picture = FileField(
        "Profile Picture",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Only JPG, JPEG, and PNG images are allowed."
            )
        ]
    )

    submit = SubmitField("Update Profile")
