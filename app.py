# CELL 14 - MAIN FLASK APPLICATION

import os
import secrets

from pathlib import Path

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user
)

from flask_wtf.csrf import CSRFProtect

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from sqlalchemy.exc import IntegrityError

from email_validator import (
    validate_email,
    EmailNotValidError
)

from forms import RegisterForm, LoginForm
from models import db, User, Student


# APPLICATION INITIALIZATION

app = Flask(
    __name__,
    instance_relative_config=True
)

os.makedirs(app.instance_path, exist_ok=True)


# SECRET KEY CONFIGURATION

secret_file = Path(app.instance_path) / "secret.key"

if not secret_file.exists():
    secret_file.write_text(
        secrets.token_hex(32),
        encoding="utf-8"
    )

app.config["SECRET_KEY"] = secret_file.read_text(
    encoding="utf-8"
).strip()


# DATABASE CONFIGURATION

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# CSRF PROTECTION

csrf = CSRFProtect(app)


# LOGIN MANAGER

login_manager = LoginManager(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(User, int(user_id))


# HOME ROUTE

@app.route("/")
def home():

    return render_template(
        "home.html",
        name="Jimrenz B. Agawa",
        section="BSECE 1C"
    )


# ABOUT ROUTE

@app.route("/about")
def about():

    return render_template("about.html")


# CONTACT ROUTE

@app.route("/contact")
def contact():

    return render_template("contact.html")


# REGISTER ROUTE

@app.route("/register", methods=["GET", "POST"])
def register():


    form = RegisterForm()

    if request.method == "POST":

        if form.validate_on_submit():
            print("Form submitted!")
        else:
            print("Validation failed.")


    if form.validate_on_submit():

        email = form.email.data.strip().lower()


        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash("Email already registered.")

            return redirect(url_for("register"))

        hashed_password = generate_password_hash(
            form.password.data
        )

        user = User(
            email=email,
            password=hashed_password
        )

        db.session.add(user)

        try:

            db.session.commit()

        except IntegrityError:

            db.session.rollback()

            flash("Unable to register this email.")

            return redirect(url_for("register"))

        flash("Registration successful!")

        return redirect(url_for("login"))

    return render_template(
        "register.html",
        form=form
    )


# LOGIN ROUTE

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data.strip().lower()

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash("Logged in successfully.")

            return redirect(url_for("students"))

        else:

            flash("Invalid email or password.")

    return render_template(
        "login.html",
        form=form
    )


# LOGOUT ROUTE

@app.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()

    flash("You have been logged out.")

    return redirect(url_for("home"))


# STUDENT LIST ROUTE

@app.route("/students")
@login_required
def students():

    student_list = Student.query.order_by(Student.full_name).all()

    return render_template(
        "students.html",
        students=student_list
    )


# ADD STUDENT ROUTE

@app.route("/add-student", methods=["POST"])
@login_required
def add_student():

    name = request.form.get("name", "").strip()

    email = request.form.get("email", "").strip()

    if not name or len(name) > 150:

        flash("Please enter a valid student name.")

        return redirect(url_for("students"))

    try:

        email = validate_email(
            email,
            check_deliverability=False
        ).normalized.lower()

        if len(email) > 150:

            raise ValueError("Email too long")

    except (EmailNotValidError, ValueError):

        flash("Please enter a valid email address.")

        return redirect(url_for("students"))

    student = Student(
        full_name=name,
        email=email
    )

    db.session.add(student)

    try:

        db.session.commit()

        flash("Student successfully added.")

    except IntegrityError:

        db.session.rollback()

        flash("Student email already exists.")

    return redirect(url_for("students"))


# DELETE STUDENT ROUTE

@app.route(
    "/delete-student/<int:id>",
    methods=["POST"]
)
@login_required
def delete_student(id):

    student = db.get_or_404(Student, id)

    db.session.delete(student)

    db.session.commit()

    flash("Student successfully deleted.")

    return redirect(url_for("students"))


# CREATE DATABASE AND RUN APPLICATION


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
