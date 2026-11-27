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
