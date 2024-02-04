from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import Length
from flask import jsonify

import getter

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with your actual secret key
app.config["WTF_CSRF_ENABLED"] = False

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False) 

# Password Validator
class PasswordValidator(FlaskForm):
    password = StringField(
        "password",
        validators=[
            validators.Length(
                min=8, message="Password must be at least 8 characters long."
            ),
            validators.Regexp(
                regex=r"^(?=.*[a-z])",
                message="Password must contain at least one lowercase letter.",
            ),
            validators.Regexp(
                regex=r"^(?=.*[A-Z])",
                message="Password must contain at least one capital letter.",
            ),
            validators.Regexp(
                regex=r"^(?=.*\d)", message="Password must contain at least one number."
            ),
        ],
    )


# Initialize Database within Application Context
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html")
def index_2():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # print(request.form)
        username = request.form["username"]
        email = request.form["email"] 
        password_validator = PasswordValidator(request.form)
        if not password_validator.validate():
            for error in password_validator.errors.values():
                flash(error[0])
            return redirect(url_for("register"))

        password = request.form["password"]
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists")
            return redirect(url_for("register"))


     # Create a new user object with username, email, and hashed password
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    # if "user_id" in session:
    #     return redirect(url_for("dashboard"))
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("mcq"))
        else:
            flash("Invalid username or password")
            return redirect(url_for("index"))


@app.route("/fb.html")
def login_page():
    return render_template("fb.html")

@app.route("/mcq")
def mcq():
    
    if "user_id" in session:
        return render_template("mcq.html", username=session["username"])
    else:
        flash("Please login first!")
        return redirect(url_for("index"))

@app.route("/mcq.html")
def mcq_page():
    return render_template("mcq.html")
@app.route("/match.html")
def match():
    return render_template("match.html")


section_scores = {
    "section_1": 0,
    "section_2": 0,
    "section_3": 0
}

@app.route("/save_score", methods=["POST"])

def save_score():
    data = request.json
    section_name = data.get("section_name")
    score = data.get("score")
    print(f"Received score for {section_name}: {score}")
    section_scores[section_name] = score
    # Perform additional processing or save to a file/database as needed
    return jsonify({"message": "Score saved successfully"})

@app.route("/get_scores")
def get_scores():
    # Return the section scores as JSON
    return jsonify(section_scores)

@app.route("/dashboard.html")
def dash_board():
    return render_template("dashboard.html")
if __name__ == "__main__":
    app.run(debug=True)
