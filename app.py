"""
Flask creates the instance of WSGI application
"""
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


from models import User


@app.route("/")
def index():
    users = User.query.all()
    for user in users:
        print(user.username)
    """This view function is for the home page"""
    return render_template("index.html")


@app.route("/<cat>")
def topic(cat):
    """This view function is for Category posts page"""
    return render_template("topic.html", cat=cat)


@app.route("/submit")
def submit():
    """This view function is for the submit page"""
    return render_template("submit.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """This view function is for the submit page"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # login successful
            return redirect(url_for("index"))
        else:
            # login failed
            return render_template("login.html", error=True)
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """dkdk"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html")


# html escaping
# @app.route("/<name>")
# def hello(name):
#     """Test function only"""
#     return f"I am {escape(name)}"
